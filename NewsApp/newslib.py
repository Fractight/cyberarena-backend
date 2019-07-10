import requests

def get_news(group_domain, token, step=20):
    params = {'domain': group_domain, 'v': '5.101', 'access_token': token, 'count': 20, 'offset': 0}
    news = []
    count_max = float('inf')
    while params.get('offset') < count_max:
        response = requests.get("https://api.vk.com/method/wall.get", params)
        response = response.json()
        news += _parse_news(response)

        count_max = response.get('count')
        params['offset'] += step

    return news

def _parse_news(response):
    items = response.get('response').get('items')
    news = []
    for post in items:
        parsed_post = {
            'text': post.get('text'),
            'date': post.get('date'),
            'attachments': [a.get('photo') for a in post.get('attachments') if a.get('type')=='photo']
        }

        news.append(parsed_post)
    print(news)
    return news


print(get_news('pkst1692', "29f249fa8676d4e701852e65db415700a163138a4ba147ab32880cf797896a06a438cdac952d40930aaa6"))
