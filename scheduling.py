from UserApp.schedule_funcs import *
from NewsApp.schedule_funcs import *
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_items, 'interval', seconds=3600)
scheduler.add_job(refresh_news, 'interval', seconds=3600)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())