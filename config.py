import os
import datetime


class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = "afsedjyfg23h72"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    JWT_SECRET_KEY = 'qsdadqw123ftru365kfsseak5'
    JWT_ACCESS_TOKEN_EXPIRES = False

    VK_CLIENT_ID = 6983724
    VK_CLIENT_SECRET = 'O24pgK0wTIa0JpivuUvi'
    VK_TOKEN = "29f249fa8676d4e701852e65db415700a163138a4ba147ab32880cf797896a06a438cdac952d40930aaa6"
    VK_GROUP_DOMAIN = 'pkst1692'

    UPLOADED_IMAGES_DEST = 'static/images'
    UPLOADED_IMAGES_URL = '/static/images/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class LocalConfig(Config):
    DEBUG = True
    DOMAIN = 'http://25.55.106.136:5000'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:l1light2KiRa@localhost:3306/cyberarena"


class ProductionConfig(Config):
    DEBUG = False
    DOMAIN = 'https://pymole.pythonanywhere.com'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://Pymole:l1light2KiRa@Pymole.mysql.pythonanywhere-services.com/Pymole$cyberarena"
