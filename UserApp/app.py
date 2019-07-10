from flask import Blueprint
from flask_restful import Api
from settings import app, db
from .models import User, Role
from flask_jwt_extended import JWTManager
from flask_security import SQLAlchemyUserDatastore, Security

users_bp = Blueprint('users', __name__)
api = Api(users_bp)
app.register_blueprint(users_bp, url_prefix='/user')

jwt = JWTManager(app)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.before_first_request
def before_first_request():
    # Create the Roles
    user_datastore.find_or_create_role(name='admin', description='Have access to admin panel')
    user_datastore.find_or_create_role(name='editor', description='Can edit database')
    user_datastore.find_or_create_role(name='mobile user', description='Standard mobile user')

    db.session.commit()

    if not User.query.filter_by(login='superadmin').first():
        user_datastore.create_user(login='superadmin', password='password',
                                              roles=['admin', 'editor'])

    if not User.query.filter_by(login='test user').first():
        user_datastore.create_user(login='test user', password='password',
                                             roles=['mobile user'])

    if not User.query.filter_by(login='staff').first():
        user_datastore.create_user(login='staff', password='password',
                                             roles = ['admin'])

    db.session.commit()

from . import routes