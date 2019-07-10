from .app import api
from .resources.NewsResource import NewsResource

api.add_resource(NewsResource, '')