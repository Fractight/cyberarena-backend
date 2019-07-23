from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads, patch_request_class

app = Flask(__name__)
app.config.from_object('config.LocalConfig')

db = SQLAlchemy()
db.init_app(app)
ma = Marshmallow()

images = UploadSet('images', IMAGES, app.config['UPLOADED_IMAGES_DEST'])  # создаем сет для картинок
configure_uploads(app, (images,))        # получаем конфигурации всех сетов
patch_request_class(app, 16 * 1024 * 1024)  # патчим werkzeug, чтобы большие файлы отклюнялись


class Settings(db.Model):
    __tablename__ = 'settings'
    latest_news_date = db.Column(db.Integer(), primary_key=True)


from UserApp import app as user_app
from ImageApp import app as image_app
from CaseApp import app as case_app
from AdminApp import app as admin_app
from NewsApp import app as news_app

import scheduling

