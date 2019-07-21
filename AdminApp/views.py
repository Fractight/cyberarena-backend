from flask import redirect, request, url_for, flash, render_template, abort
from flask_admin import expose, AdminIndexView, BaseView, form
from flask_admin.contrib.sqla import ModelView as BaseModelView
from flask_security import login_user, logout_user, current_user
from http import HTTPStatus

from .forms import AdminLoginForm, SearchItemCodeForm, ConfirmItemForm
from UserApp.models import User
from CaseApp.models import Inventory, ItemSchema, Item
from settings import db, app
from AdminApp.utils import list_thumbnail, imagename_uuid1_gen

item_schema = ItemSchema(many=True)


@app.route('/admin/login', endpoint='admin.login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm(request.form)
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(login=form.username.data).first()
        if user is None or not user.verify_hash(form.password.data):
            flash('Invalid username or password')
            return render_template('admin/login.html', form=form)

        login_user(user, remember=form.remember_me)
        return redirect(url_for('admin.index'))

    return render_template('admin/login.html', form=form)


@app.route('/admin/logout', endpoint='admin.logout', methods=['GET'])
def admin_login():
    logout_user()
    return redirect(url_for('admin.login'))


class AdminSecurityMixin:

    def is_accessible(self):
        if (current_user.is_active and current_user.is_authenticated
                and current_user.has_role('admin')):
            return True
        return False

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(HTTPStatus.FORBIDDEN)
            return redirect(url_for('admin.login'))


class EditorSecurityMixin(AdminSecurityMixin):
    def is_accessible(self):
        return (current_user.is_active and current_user.is_authenticated
            and current_user.has_role('admin') and current_user.has_role('editor'))


class ModelView(EditorSecurityMixin, BaseModelView):
    pass


class UserModelView(ModelView):
    column_list = ('login', '_password', 'roles', 'active')
    form_columns = ('login', 'password', 'roles', 'active')


class InventoryModelView(ModelView):
    column_list = ('user', 'item', 'code', 'expiration')
    form_columns = ('user', 'item', 'code', 'expiration')


class ItemModelView(ModelView):
    column_list = ('name', 'description',
                   'probability', 'expiration_period', 'case', 'image')
    form_columns = ('name', 'description', 'probability',
                    'expiration_period', 'case', 'image')


class AdminView(AdminSecurityMixin, AdminIndexView):
    @expose('/')
    def index(self):
        return super(AdminView, self).index()


class ExchangeView(AdminSecurityMixin, BaseView):
    @expose('/', methods=['GET', 'POST'])
    def exchange(self):
        search_form = SearchItemCodeForm()
        if search_form.validate_on_submit():
            # check if code exists
            print(search_form.code.data)
            item = Inventory.query.filter_by(code=search_form.code.data).first()
            if not item:
                return self.render('admin/no_item.html')

            return redirect(url_for('.confirm', inventory_item_id=item.id))

        return self.render('admin/exchange.html', form=search_form)

    @expose('/confirm', methods=['GET', 'POST'])
    def confirm(self):
        inventory_item_id = request.args.get('inventory_item_id')
        confirm_form = ConfirmItemForm(item_id=inventory_item_id)
        inventory_item = Inventory.query.filter_by(id=inventory_item_id).first()

        if confirm_form.validate_on_submit():
            db.session.delete(inventory_item)
            db.session.commit()
            return redirect(url_for('.exchange'))

        item_type = Item.query.get(inventory_item.item_id)
        item_type_info = item_schema.dump(item_type).data
        print(item_type_info)

        return self.render('admin/confirm_item.html', form=confirm_form, item_info=item_type_info)


class ImageView(ModelView):

    column_list = [
        'image', 'name', 'filename', 'size'
    ]

    column_formatters = {
        'image': list_thumbnail
    }

    form_extra_fields = {
        'filename': form.ImageUploadField(
            'Image',
            base_path=app.config['UPLOADED_IMAGES_DEST'],
            url_relative_path='images/',
            namegen=imagename_uuid1_gen,
        )
    }