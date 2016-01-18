from app.db import Base
from app.db import BaseModelObject
from app.utils.crypto import authenticate_password
from app.utils.crypto import hash_password

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID

from uuid import uuid4


class User(Base, BaseModelObject):
    __tablename__ = 'users'
    uuid = Column(UUID, primary_key=True)
    email = Column(String(120), unique=True)
    name = Column(String(500))
    password_hash = Column(String(60), unique=False)
    active = Column(Boolean(), default=False, nullable=False)
    phone_number = Column(String(128))
    email_verification_token = Column(String(50), unique=False)
    dead = Column(Boolean(), default=False, nullable=False)
    created_at = Column(DateTime(), unique=False)

    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.uuid)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def activate(self):
        self.update(active=True)

    def update_password(self, new_password):
        new_password = hash_password(new_password)
        self.update(password_hash=new_password)

    @staticmethod
    def update_user(uuid, **kwargs):
        user = User.get(uuid=uuid)
        if not user:
            return None

        if kwargs.get('password'):
            kwargs['password_hash'] = hash_password(kwargs['password'])

        email = kwargs.get('email')
        if email and user.email != email:
            other_user = User.get(email=email)
            if other_user and other_user != user:
                raise Exception("A user with this email address already exists: {}".format(email))

        user.update(**kwargs)
        return user

    @staticmethod
    def create_user(email, name=None, password_hash=None):
        user = User.get(email=email)
        if user:
            if user.dead:
                user.update(dead=False)
                return user
            raise Exception('A User with that email has already been created.')
        user = User.create(email=email,
                           name=name,
                           password_hash=password_hash,
                           email_verification_token=str(uuid4()),
                           active=False)
        return user

    @staticmethod
    def verify_user(uuid, password):
        user = User.get(uuid=uuid)
        if user:
            verified = authenticate_password(password, user.password_hash.encode('utf-8'))
            if verified:
                return user
        raise Exception("Incorrect password.")

    @staticmethod
    def get_verified_user(email, password):
        user = User.get(email=email, active=True, dead=False)
        if user:
            verified = authenticate_password(password, user.password_hash.encode('utf-8'))
            if verified:
                return user
        return None
