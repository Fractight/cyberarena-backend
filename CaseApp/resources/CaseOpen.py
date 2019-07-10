from flask_restful import Resource
from CaseApp.models import Case, CaseSchema, Item, ItemSchema, Inventory
from UserApp.models import User
from settings import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from random import choices

cases_schema = CaseSchema(many=True)
case_schema = CaseSchema()

item_schema = ItemSchema()

class CaseOpen(Resource):
    @jwt_required
    def post(self, case_id):
        case = Case.query.get(case_id)
        if not case:
            return {'message': "Case doesn't exists"}, 400

        items = Item.query.filter_by(case_id=case_id)

        items = [item for item in items]
        p_distr = [item.probability for item in items]

        reward = choices(population=items, weights=p_distr)[0]

        user_login = get_jwt_identity()
        user_id = User.find_by_login(login=user_login).id

        inv = Inventory(
            user_id = user_id,
            item_id = reward.id
        )

        db.session.add(inv)
        db.session.commit()

        reward = item_schema.dumps(reward).data

        return { "status": 'success', 'reward': reward }, 201