import requests

def get_news(group_domain, token, from_date=0, step=20):
    params = {'domain': group_domain, 'v': '5.101', 'access_token': token,
              'count': 20, 'offset': 0}
    news = []
    count_max = float('inf')
    continue_flag = True
    while params['offset'] < count_max and continue_flag:
        response = requests.get("https://api.vk.com/method/wall.get", params)
        response = response.json().get('response')
        continue_flag, parsed_news = _parse_news(response, from_date)
        news += parsed_news

        count_max = response.get('count')
        params['offset'] += step

    news.reverse()
    return news

def _parse_news(response, from_date=0):
    items = response.get('items')
    news = []

    for post in items:
        date = post.get('date')
        if from_date >= date:
            return False, news

        parsed_post = {
            'text': post.get('text'),
            'date': date,
            'attachments': [a.get('photo') for a in post.get('attachments', []) if a.get('type')=='photo']
        }

        news.append(parsed_post)

    return True, news