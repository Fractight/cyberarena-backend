from flask import request
from flask_restful import Resource
from CaseApp.models import Case, Item, CaseSchema, ItemSchema
from UserApp.models import User
from settings import db
from flask_jwt_extended import jwt_required, get_jwt_identity

cases_schema = CaseSchema(many=True)
case_schema = CaseSchema()

items_schema = ItemSchema(many=True)


class CaseInfo(Resource):
    @jwt_required
    def get(self, case_id):
        user_id = User.find_by_login(get_jwt_identity()).id

        case = Case.query.get(case_id)
        if case is None:
            return {"error": "Case doen't exists"}

        items = Item.query.filter_by(case_id=case_id)
        items = items_schema.dump(items).data

        return {'case': case.json_with_cooldown(user_id), 'items': items}, 200
