from flask_restful import Resource
from CaseApp.models import InventorySchema, Inventory
from UserApp.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

inventory_schema = InventorySchema(many=True)

class ItemsInfo(Resource):
    @jwt_required
    def get(self):
        user_login = get_jwt_identity()
        user = User.find_by_login(user_login)

        items = Inventory.query.filter_by(user_id = user.id)
        items = inventory_schema.dump(items).data

        return {'items': items}, 201