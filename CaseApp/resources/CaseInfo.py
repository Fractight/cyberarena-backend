from flask import request
from flask_restful import Resource
from CaseApp.models import Case, CaseSchema, Item, ItemSchema
from settings import db
from flask_jwt_extended import jwt_required

cases_schema = CaseSchema(many=True)
case_schema = CaseSchema()

items_schema = ItemSchema(many=True)

class CaseInfo(Resource):
    @jwt_required
    def get(self, case_id):
        case = Case.query.get(case_id)
        items = Item.query.filter_by(case_id=case.id)

        case = case_schema.dump(case).data
        items = items_schema.dump(items).data

        return {'case': case, 'items': items}, 200
