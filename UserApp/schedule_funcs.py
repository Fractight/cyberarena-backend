from settings import app
from CaseApp.models import Inventory

def delete_expired_items():
    with app.app_context():
        rows_deleted = Inventory.query.filter(Inventory.is_expired).delete()
        print(rows_deleted)