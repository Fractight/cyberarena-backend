from flask_restful import Resource
from CaseApp.models import ItemSchema, Inventory
from UserApp.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

items_schema = ItemSchema(many=True)
item_schema = ItemSchema()

class ItemActivate(Resource):
    @jwt_required
    def patch(self, item_id):
        user_id = User.find_by_login(get_jwt_identity()).id
        item = Inventory.query.get(item_id)
        if not item or item.user_id != user_id:
            return {'message': 'No item inside inventory'}, 400

        if item.code is not None:
            return {'message': 'Item already activated'}, 400

        # create code and expiration for item
        response = item.activate()

        return response, 200
