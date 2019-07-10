from CaseApp.models import Inventory
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from settings import app

def delete_expired_items():
    with app.app_context():
        rows_deleted = Inventory.query.filter(Inventory.is_expired).delete()
        print(rows_deleted)

scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_items, 'interval', seconds=3600)
scheduler.start()

atexit.register(lambda: scheduler.shutdown())