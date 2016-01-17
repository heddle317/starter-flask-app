from app import app
from app import config

from flask_assets import Bundle
from flask_assets import Environment


assets = Environment(app)

base_css = Bundle('css/external/bootstrap.min.css',
                  'css/external/font-awesome.min.css',
                  'css/internal/base.css',
                  filters='cssmin', output='gen/base.%(version)s.css')

assets.register('base_css', base_css)

if config.ENV == 'production':
    base_js = Bundle('js/external/jquery-1.11.1.min.js',
                     'js/external/bootstrap.min.js',
                     filters='jsmin', output='gen/base.%(version)s.js')
else:
    base_js = Bundle('js/external/jquery-1.11.1.min.js',
                     'js/external/bootstrap.min.js',
                     output='gen/base.%(version)s.js')

assets.register('base_js', base_js)
