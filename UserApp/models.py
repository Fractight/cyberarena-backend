from marshmallow import fields
from flask_security import UserMixin, RoleMixin
from passlib.hash import sha256_crypt
from settings import db, ma
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
)


# Role class
class Role(db.Model, RoleMixin):

    # Our Role has three fields, ID, name and description
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # __str__ is required by Flask-Admin, so we can have human-readable values for the Role when editing a User.
    def __str__(self):
        return self.name

    # __hash__ is required to avoid the exception TypeError: unhashable type: 'Role' when saving a User
    def __hash__(self):
        return hash(self.name)


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(255), unique=True, nullable=False)  # user - vk_id; admin - login
    _password = db.Column(db.Text, nullable=False)  # user - vk_access_token; admin - password
    email = db.Column(db.String(255), unique=True)
    active = db.Column(db.Boolean(), nullable=False)

    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic')
    )

    def __init__(self, login='', password='', active=True, roles=[]):
        self.login = login
        self.password = password
        self.active = active
        self.roles = roles

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = sha256_crypt.hash(password)

    @hybrid_method
    def verify_hash(self, password):
        return sha256_crypt.verify(password, self._password)

    @staticmethod
    def find_by_login(login):
        return User.query.filter_by(login=login).first()


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User




