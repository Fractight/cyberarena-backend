from flask_restful import Resource
from CaseApp.models import InventorySchema, Inventory
from UserApp.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

inventory_schema = InventorySchema(many=True)


class ItemsInfo(Resource):
    @jwt_required
    def get(self):
        offset = request.args.get('offset')
        count = request.args.get('count')

        if offset is None:
            offset = 0
        else:
            try:
                offset = int(offset)
            except:
                return {'error': 'Offset could be an integer'}

        if count is None:
            count = 1
        else:
            try:
                count = int(count)
            except:
                return {'error': 'Count could be an integer'}

        count = max(1, min(20, count))
        offset = max(0, offset)

        user_login = get_jwt_identity()
        user = User.find_by_login(user_login)

        items = Inventory.query.filter_by(user_id=user.id).limit(count).offset(offset).all()
        items = inventory_schema.dump(items).data

        return {'items': items}, 201