from flask import request as flask_request
from flask import url_for, redirect
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from UserApp.models import User, UserSchema
from settings import db, app
from UserApp.app import user_datastore
import requests

class VKAuth(Resource):
    def get(self):
        code = flask_request.args.get('code')
        if code is None:
            return {'message': 'Authorization error'}, 400

        # get user vk access token and id
        response = requests.get(
            'https://oauth.vk.com/access_token',
            params={
                'client_id': app.config.get('VK_CLIENT_ID'),
                'client_secret': app.config.get('VK_CLIENT_SECRET'),
                'redirect_uri': url_for('.vkauth', _external=True, _scheme='http'),
                'code': code,
            }
        )

        response = response.json()
        if 'error' in response:
            return {'message': 'Authorization error'}, 400

        user_id = str(response.get('user_id'))
        if not User.query.filter_by(login=user_id).first():
            user_datastore.create_user(
                login = user_id,
                password = response.get('access_token'),
                roles = ['mobile user']
            )

            db.session.commit()

        access_token = create_access_token(identity=user_id)
        refresh_token = create_refresh_token(identity=user_id)

        return redirect(url_for('user.token_redirect', access_token=access_token, refresh_token=refresh_token))

@app.route('/user/vkauth/token/', endpoint='user.token_redirect', methods=['GET'])
def token_redirect():
    return ''
