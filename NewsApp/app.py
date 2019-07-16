from flask import Blueprint
from flask_restful import Api
from settings import app, db
from .models import News

news_bp = Blueprint('news_app', __name__)
api = Api(news_bp)
app.register_blueprint(news_bp, url_prefix='/news')

from .routes import *