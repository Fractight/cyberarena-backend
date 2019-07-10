from flask_restful import Resource
from NewsApp.models import News
from flask import request

class NewsResource(Resource):
    def get(self):
        offset = request.args.get('offset')
        count = request.args.get('count')

        if offset is None:
            offset = 0
        else:
            try:
                offset = int(offset)
            except:
                return {'error': 'Offset could be an integer'}

        if count is None:
            count = 1
        else:
            try:
                count = int(count)
            except:
                return {'error': 'Count could be an integer'}

        count = max(1, min(20, count))
        offset = max(0, offset)

        print(offset, count)
        news_query = News.query.offset(offset).limit(count).all()
        return {'news': [n.vk_json for n in news_query]}, 200
