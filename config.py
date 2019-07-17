import os
import datetime

# You need to replace the next values with the appropriate values for your configuration

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SECRET_KEY = "afsedjyfg23h72"
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:l1light2KiRa@localhost:3306/cyberarena"
JWT_SECRET_KEY = 'qsdadqw123ftru365kfsseak5'
VK_CLIENT_ID = 6983724
VK_CLIENT_SECRET = 'O24pgK0wTIa0JpivuUvi'
VK_TOKEN = "29f249fa8676d4e701852e65db415700a163138a4ba147ab32880cf797896a06a438cdac952d40930aaa6"
VK_GROUP_DOMAIN = 'pkst1692'

JWT_ACCESS_TOKEN_EXPIRES = False