from flask_admin.menu import MenuLink
from flask_admin import Admin
from settings import app
from .views import *
from UserApp.models import User
from CaseApp.models import Item, Case, Inventory
from NewsApp.models import News
from ImageApp.models import Image

admin = Admin(app, index_view=AdminView())
admin.add_view(UserModelView(User, db.session))
admin.add_view(ItemModelView(Item, db.session))
admin.add_view(ModelView(Case, db.session))
admin.add_view(InventoryModelView(Inventory, db.session))
admin.add_view(ModelView(News, db.session))
admin.add_view(ImageView(Image, db.session))

admin.add_view(ExchangeView(name='Exchange', endpoint='exchange'))

admin.add_link(MenuLink(name='Logout', category='', url='/admin/logout'))