from flask_restful import Resource
from CaseApp.models import Case, CaseSchema, Item, ItemSchema
from settings import db
from flask_jwt_extended import jwt_required

cases_schema = CaseSchema(many=True)
case_schema = CaseSchema()

items_schema = ItemSchema(many=True)

class CasesInfo(Resource):
    @jwt_required
    def get(self):
        # all cases
        cases = Case.query.all()
        cases = cases_schema.dump(cases).data
        return {'cases':cases}, 200