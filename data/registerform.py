from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import EmailField, IntegerField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    name = StringField('Имя пользователя', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    surname = StringField('Фамилия пользователя', validators=[DataRequired()])
    age = IntegerField('Возвраст пользователя', validators=[DataRequired()])
    position = StringField('Позиция пользователя', validators=[DataRequired()])
    speciality = StringField('Професия пользователя', validators=[DataRequired()])
    address = StringField('Адресс пользователя', validators=[DataRequired()])
    submit = SubmitField('Зарегестрироваться')
