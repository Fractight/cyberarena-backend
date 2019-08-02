from flask_restful import Resource
from CaseApp.models import Case, CaseSchema, Item, ItemSchema, Inventory, CaseCooldown
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
        # check case existence
        case = Case.query.get(case_id)
        if not case:
            return {'error': "Case doesn't exists"}, 400

        user_login = get_jwt_identity()
        user_id = User.find_by_login(login=user_login).id

        # check case cooldown
        case_cooldown = CaseCooldown.query.filter_by(case_id=case_id, user_id=user_id).first()
        if case_cooldown is not None:
            if case_cooldown.is_cooled_down:
                db.session.delete(case_cooldown)
            else:
                return {'error': "Case isn't cooled down"}, 400

        items = Item.query.filter_by(case_id=case_id)
        items = [item for item in items]
        p_distr = [item.probability for item in items]

        reward = choices(population=items, weights=p_distr)[0]

        # create new item
        inv = Inventory(
            user_id=user_id,
            item_id=reward.id
        )
        db.session.add(inv)

        # case cool down after opening
        case_cooldown = CaseCooldown(
            user_id=user_id,
            case_id=case_id
        )
        db.session.add(case_cooldown)

        db.session.commit()

        reward = item_schema.dump(reward).data

        return {'reward': reward}, 201
