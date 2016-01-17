import os

ENV = os.environ.get('ENVIRONMENT', 'dev')

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
ROOT_PATH = BASE_DIR = os.path.join(os.path.dirname(__file__), '..')

STATIC_FOLDER = os.path.join(ROOT_PATH, 'static')
TEMPLATE_FOLDER = os.path.join(ROOT_PATH, 'templates')
SECRET_KEY = os.environ.get('SECRET_KEY')
CSRF_ENABLED = True
MODEL_HASH = os.environ.get('MODEL_HASH')

SQLALCHEMY_MIGRATE_REPO = os.path.join(ROOT_PATH, 'db_repository')
SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_TRACK_MODIFICATIONS = False

if ENV == 'dev':
    PORT = 7000
    APP_BASE_LINK = 'http://localhost:' + str(PORT)
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/deploy_db'
    LOG_PATH = os.path.join(ROOT_PATH, 'logs')
else:
    LOG_PATH = '/var/log'
    APP_BASE_LINK = 'https://baselink.com'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(os.environ.get('POSTGRES_ENV_POSTGRES_USER'),
                                                                   os.environ.get('POSTGRES_ENV_POSTGRES_PASSWORD'),
                                                                   os.environ.get('POSTGRES_PORT_5432_TCP_ADDR'),
                                                                   os.environ.get('POSTGRES_PORT_5432_TCP_PORT'),
                                                                   os.environ.get('POSTGRES_ENV_POSTGRESQL_DB'))

