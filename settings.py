from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy()
db.init_app(app)
ma = Marshmallow()

class Settings(db.Model):
    __tablename__ = 'settings'
    latest_news_date = db.Column(db.Integer(), primary_key=True)

from UserApp import app as user_app
from CaseApp import app as case_app
from AdminApp import app as admin_app
from NewsApp import app as news_app
import scheduling

