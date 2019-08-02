from settings import app, db
from CaseApp.models import Inventory


def delete_expired_items():
    with app.app_context():
        rows_deleted = Inventory.query.filter(Inventory.is_expired).delete()
        db.session.commit()
        print(rows_deleted)
