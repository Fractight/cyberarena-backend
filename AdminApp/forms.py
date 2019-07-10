from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired

class AdminLoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')

class SearchItemCodeForm(FlaskForm):
    code = StringField('Код', validators=[DataRequired()])
    submit = SubmitField('Проверить')

class ConfirmItemForm(FlaskForm):
    item_id = HiddenField(validators=[DataRequired()])
    submit = SubmitField('Подтвердить')
