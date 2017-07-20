# coding:utf-8

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextAreaField, SubmitField, \
    PasswordField, SelectMultipleField, FieldList
from wtforms.validators import DataRequired, Length, Email, EqualTo




class TaxForm(FlaskForm):
    envs = StringField(u'环境', validators=[DataRequired()])
    description = TextAreaField(u'环境说明')
