from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class CheckoutForm(FlaskForm):
    submit = SubmitField('Оплатить')