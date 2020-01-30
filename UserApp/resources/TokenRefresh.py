from flask_restful import Resource
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def get(self):
        user_login = get_jwt_identity()
        access_token = create_access_token(identity=user_login)
        return {'access_token': access_token}, 200
