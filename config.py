import os
import datetime
import secret_config


class Config(secret_config.Config):
    basedir = os.path.abspath(os.path.dirname(__file__))

    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    JWT_ERROR_MESSAGE_KEY = 'error'

    VK_GROUP_DOMAIN = 'pkst1692'

    UPLOADED_IMAGES_DEST = 'static/images'
    UPLOADED_IMAGES_URL = '/static/images/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class DevelopmentConfig(Config, secret_config.DevelopmentConfig):
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = False


class ProductionConfig(Config, secret_config.ProductionConfig):
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)