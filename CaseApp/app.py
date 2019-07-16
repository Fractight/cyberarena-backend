from flask import Blueprint
from flask_restful import Api
from settings import app

cases_bp = Blueprint('shop', __name__)
api = Api(cases_bp)
app.register_blueprint(cases_bp, url_prefix='/shop')

from flask_jwt_extended import JWTManager
jwt = JWTManager(app)

from .routes import *
