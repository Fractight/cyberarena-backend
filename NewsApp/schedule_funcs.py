from .models import News
from settings import app, db, Settings
from NewsApp import newslib
from sqlalchemy.orm import load_only

def refresh_news():
    with app.app_context():
        sets = Settings.query.options(load_only(Settings.latest_news_date)).one()
        print(sets)

        news = newslib.get_news(
            app.config['VK_GROUP_DOMAIN'],
            app.config['VK_TOKEN'],
            from_date=sets.latest_news_date
        )

        if news:
            # change latest date
            sets.latest_news_date = news[-1].get('date')

            for n in news:
                db.session.add(News(vk_json=n))

            db.session.commit()
