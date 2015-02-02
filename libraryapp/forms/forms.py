# -*- coding: utf-8 -*-

from flask_wtf import Form, BooleanField, TextField, PasswordField, TextAreaField, validators
from wtforms.validators import Required, Length
from flask.ext.babel import gettext
from libraryapp.models.modelapp import User


class LoginForm(Form):
    login = TextField('login', validators=[Required()])
    password = PasswordField('password', validators=[Required()])
    remember_me = BooleanField('remember_me', default=False)


class RegistrationForm(Form):
    username = TextField(u'Введите логин', [validators.Length(min=4, max=25)])
    password = PasswordField(u'Введите пароль', [
        validators.Required(),
        validators.EqualTo('confirm', message=u'Пароли должны совпадать')
    ])
    confirm = PasswordField(u'Повторите Ваш пароль еще раз')


class AskQuestionForm(Form):
    question = TextField(u'Введите вопрос', [validators.Length(min=10, max=128)])


class AnswerForm(Form):
    body = TextAreaField(u'Напишите ответ', [validators.optional(), validators.length(max=512)])
