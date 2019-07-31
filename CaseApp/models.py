from marshmallow import fields
from sqlalchemy.ext.hybrid import hybrid_property
from settings import db, ma
import secrets
from string import ascii_uppercase, digits
import datetime
from ImageApp.models import ImageSchema

code_simbols = ascii_uppercase + digits


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    probability = db.Column(db.Float, nullable=False)
    expiration_period = db.Column(db.Integer, default=3600)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    image = db.relationship('Image', backref=db.backref('item_image'))
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id', ondelete='CASCADE'))

    def __str__(self):
        return str(self.name) + ', ' + str(self.id)


class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    image = db.relationship('Image', backref=db.backref('case_image'))
    items = db.relationship('Item', backref=db.backref('case'))

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
        if self.expiration is None:
            return None
        return (self.expiration - datetime.datetime.now()).total_seconds()


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item

    image = ma.Method('image_url')

    def image_url(self, obj):
        return None if obj.image is None else obj.image.url


class CaseSchema(ma.ModelSchema):
    class Meta:
        model = Case
        exclude = ('items',)

    image = ma.Method('image_url')

    def image_url(self, obj):
        return None if obj.image is None else obj.image.url


class InventorySchema(ma.ModelSchema):
    class Meta:
        model = Inventory
        fields = ('id', 'expires_in', 'code', 'item')

    item = ma.Nested(ItemSchema)



