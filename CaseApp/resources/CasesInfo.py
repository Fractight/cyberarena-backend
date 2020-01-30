from flask_restful import Resource
from CaseApp.models import Case
from UserApp.models import User
from settings import db
from flask_jwt_extended import jwt_required, get_jwt_identity


class CasesInfo(Resource):
    @jwt_required
    def get(self):
        # all cases
        cases = Case.query.all()
        user_id = User.find_by_login(get_jwt_identity()).id

        return {
            'cases': [
                case.json_with_cooldown(user_id)
                for case in cases
            ]
        }, 200