from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from UserApp.models import User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()

class UserProfile(Resource):
    @jwt_required
    def get(self):
        user = User.find_by_login(get_jwt_identity())
        user_info = user_schema.dump(user).data

        return {'user_info':user_info}, 200
