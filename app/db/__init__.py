from app import db
from app.utils.datetime_tools import format_date
from app.utils.datetime_tools import now_utc

from sqlalchemy.orm import class_mapper
from sqlalchemy.ext.declarative import declarative_base

from uuid import uuid4

Base = declarative_base()


def get(model, **kwargs):
    sort_by = kwargs.pop('sort_by', 'created_at')
    desc = kwargs.pop('desc', True)
    items = db.session.query(model).filter_by(**kwargs)
    if hasattr(model, sort_by):
        order_by = getattr(model, sort_by)
        if desc:
            items = items.order_by(order_by.desc().nullslast())
        else:
            items = items.order_by(order_by.asc().nullslast())
    return items.first()


def get_list(model, raw=False, **kwargs):
    sort_by = kwargs.pop('sort_by', 'created_at')
    limit = kwargs.pop('limit', None)
    desc = kwargs.pop('desc', True)
    items = db.session.query(model)

    list_keys = []
    for key, value in kwargs.iteritems():
        if isinstance(value, list):
            field = getattr(model, key)
            items = items.filter(field.in_(kwargs.get(key)))
            list_keys.append(key)
    for key in list_keys:
        kwargs.pop(key)

    items = items.filter_by(**kwargs)
    if hasattr(model, sort_by):
        order_by = getattr(model, sort_by)
        if desc:
            items = items.order_by(order_by.desc().nullslast())
        else:
            items = items.order_by(order_by.asc().nullslast())
    items = items.limit(limit)
    if raw:
        return items
    return items.all()


def save(obj, refresh=True):
    obj = db.session.merge(obj)
    db.session.commit()

    if refresh:
        db.session.refresh(obj)

    return obj


def publish(obj):
    update(obj, {'publish`': True})
    save(obj)


def delete(obj, hard_delete=False):
    db.session.delete(obj)
    db.session.commit()


def update(obj, data):
    changed = False

    for field, val in data.items():
        if hasattr(obj, field) and not field == 'uuid':
            setattr(obj, field, val)
            changed = True

    if changed:
        return save(obj)

    return obj


def create(model, **kwargs):
    m = model()
    if hasattr(m, 'uuid'):
        m.uuid = str(uuid4())
    if hasattr(m, 'created_at'):
        m.created_at = now_utc()
    for k, v in kwargs.items():
        if hasattr(m, k):
            setattr(m, k, v)

    return save(m, refresh=True)


def jsonify_model(obj):
    if obj is None:
        return {}
    if isinstance(obj, list):
        items = [item.to_dict() for item in obj]
        return items
    return obj.to_dict()


class BaseModelObject(object):

    def to_dict(self):
        attr_dict = {}
        keys = [col.key for col in class_mapper(self.__class__).iterate_properties]
        for key in keys:
            attr_dict[key] = getattr(self, key)
        if hasattr(self, 'created_at'):
            attr_dict['created_at'] = format_date(self.created_at, '%a, %d %b %Y %H:%M:%S')
        return attr_dict

    @classmethod
    def get_list(cls, to_json=False, dead=False, **kwargs):
        if hasattr(cls, 'dead'):
            items = get_list(cls, dead=dead, **kwargs)
        else:
            items = get_list(cls, **kwargs)
        return jsonify_model(items) if to_json else items

    @classmethod
    def get(cls, to_json=False, dead=False, **kwargs):
        if hasattr(cls, 'dead'):
            item = get(cls, dead=dead, **kwargs)
        else:
            item = get(cls, **kwargs)
        return jsonify_model(item) if to_json else item

    @classmethod
    def get_or_404(cls, to_json=False, dead=False, **kwargs):
        item = cls.get(to_json=to_json, dead=dead, **kwargs)
        if not item:
            from flask import abort
            abort(404)
        return item

    @classmethod
    def create(cls, **kwargs):
        item = create(cls, **kwargs)
        return item

    @classmethod
    def get_or_create(cls, **kwargs):
        item = get(cls, **kwargs)
        if not item:
            item = create(cls, **kwargs)
        return item

    @classmethod
    def delete_all(cls, **kwargs):
        items = get_list(cls, **kwargs)
        for item in items:
            item.delete()

    def update(self, **kwargs):
        item = update(self, kwargs)
        return item

    def delete(self):
        if hasattr(self, 'dead'):
            update(self, {'dead': True})
        else:
            delete(self)
