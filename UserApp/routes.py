from .app import api
from settings import app

from .resources.UserProfile import UserProfile
from .resources.VKAuth import VKAuth
from .resources.TokenRefresh import TokenRefresh

api.add_resource(UserProfile, '/profile')
api.add_resource(VKAuth, '/vk_auth')
api.add_resource(TokenRefresh, '/token_refresh')

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

from flask import url_for
@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    print(links)
    # links is now a list of url, endpoint tuples