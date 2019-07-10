from flask import request
from flask_restful import Resource
from CaseApp.models import Item, ItemSchema
from flask_jwt_extended import jwt_required
from settings import db

items_schema = ItemSchema(many=True)
item_schema = ItemSchema()

class ItemInfo(Resource):
    @jwt_required
    def get(self):
        items = Item.query.all()
        items = items_schema.dump(items).data
        return {'status': 'success', 'data': items}, 200
