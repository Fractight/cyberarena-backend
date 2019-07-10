from marshmallow import fields
from sqlalchemy.ext.hybrid import hybrid_property
from settings import db, ma
import secrets
from string import ascii_uppercase, digits
import datetime

code_simbols = ascii_uppercase + digits

class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    probability = db.Column(db.Float, nullable=False)
    expiration_period = db.Column(db.Integer, default=3600)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id', ondelete='CASCADE'), nullable=True)

    def __init__(self, name='', description='', probability=0.0, case_id=None):
        self.name = name
        self.description = description
        self.probability = probability
        self.case_id = case_id

    def __str__(self):
        return str(self.name) + ', ' + str(self.id)

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    items = db.relationship('Item', backref=db.backref('case'))

    def __init__(self, name='', description=''):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User')
    item_id = db.Column(db.Integer, db.ForeignKey('items.id', ondelete='CASCADE'), nullable=False)
    item = db.relationship('Item')
    code = db.Column(db.String(8), unique=True)
    expiration = db.Column(db.DateTime)

    def __init__(self, user_id, item_id):
        self.user_id = user_id
        self.item_id = item_id

    @hybrid_property
    def is_expired(self):
        return self.expiration is not None and self.expiration <= datetime.datetime.now()

    def activate(self):
        self.code = ''.join([secrets.choice(code_simbols) for _ in range(5)])
        self.expiration = datetime.datetime.now() + \
                          datetime.timedelta(seconds=Item.query.get(self.item_id).expiration_period)
        db.session.commit()
        return {'item_id':self.id, 'code': self.code, 'expires_in': self.expires_in}

    @hybrid_property
    def expires_in(self):
        return (self.expiration - datetime.datetime.now()).total_seconds()

class ItemSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()
    probability = fields.Float(required=True)
    case_id = fields.Integer(required=True)

class CaseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String()

class InventorySchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    item_id = fields.Integer(required=True)
