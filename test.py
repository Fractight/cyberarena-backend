from settings import app, db
from CaseApp.models import Inventory
#
# with app.app_context():
#     i = Inventory(user_id=17, item_id=1)
#     db.session.add(i)
#     db.session.commit()

with app.app_context():
    i = Inventory(user_id=17, item_id=1)

