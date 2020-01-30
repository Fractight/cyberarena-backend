from marshmallow import fields
from sqlalchemy.ext.hybrid import hybrid_property
from settings import db, ma
import secrets
from string import ascii_uppercase, digits
from datetime import datetime, timedelta
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
    cooldown_period = db.Column(db.Integer)

    image = db.relationship('Image', backref=db.backref('case_image'))
    items = db.relationship('Item', backref=db.backref('case'))

    def __str__(self):
        return self.name

    def json_with_cooldown(self, user_id):
        case_cooldown = CaseCooldown.query.filter_by(user_id=user_id).first()
        if case_cooldown is None:
            cooldown_left = 0
        else:
            cooldown_left = case_cooldown.cooldown_left

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': self.image.url,
            'cooldown_left': cooldown_left
        }


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
        return self.expiration is not None and self.expiration <= datetime.now()

    def activate(self):
        self.code = ''.join([secrets.choice(code_simbols) for _ in range(8)])
        self.expiration = datetime.now() + \
                          timedelta(seconds=Item.query.get(self.item_id).expiration_period)
        db.session.commit()
        return {'item_id': self.id, 'code': self.code, 'expires_in': self.expires_in}

    @hybrid_property
    def expires_in(self):
        if self.expiration is None:
            return None
        return (self.expiration - datetime.now()).total_seconds()


class CaseCooldown(db.Model):
    __tablename__ = 'case_cooldown'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', on_delete='CASCADE'), nullable=False)
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id', on_delete='CASCADE'), nullable=False)
    cooldown = db.Column(db.DateTime)

    user = db.relationship('User')
    case = db.relationship('Case', backref=db.backref('case_cooldowns'))

    def __init__(self, user_id, case_id):
        cooldown_period = Case.query.get(case_id).cooldown_period
        if cooldown_period is None:
            cooldown_period = 0

        self.user_id = user_id
        self.case_id = case_id
        self.cooldown = datetime.now() + timedelta(seconds=cooldown_period)

    @hybrid_property
    def is_cooled_down(self):
        return self.cooldown < datetime.now()

    @hybrid_property
    def cooldown_left(self):
        return max(0, (self.cooldown - datetime.now()).total_seconds())


class ItemSchema(ma.ModelSchema):
    class Meta:
        model = Item

    image = ma.Method('image_url')

    def image_url(self, obj):
        return None if obj.image is None else obj.image.url


class CaseSchema(ma.ModelSchema):
    class Meta:
        model = Case

    image = ma.Method('image_url')
    cooldown_left = fields.Integer()

    def image_url(self, obj):
        return None if obj.image is None else obj.image.url


class InventorySchema(ma.ModelSchema):
    class Meta:
        model = Inventory
        fields = ('id', 'expires_in', 'code', 'item')

    item = ma.Nested(ItemSchema)



