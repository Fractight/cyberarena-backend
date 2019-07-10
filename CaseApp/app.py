from flask import Blueprint
from flask_restful import Api
from settings import app

cases_bp = Blueprint('roulette', __name__)
api = Api(cases_bp)
app.register_blueprint(cases_bp, url_prefix='/roulette')

from flask_jwt_extended import JWTManager
jwt = JWTManager(app)

from .routes import *
