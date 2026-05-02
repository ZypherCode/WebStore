from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired


class AddReviewForm(FlaskForm):
    voice = RadioField('Ваш отзыв', choices=[('good','Хорошо'),('bad','Плохо')])
    content = TextAreaField("Ваш отзыв")
    submit = SubmitField('Оставить отзыв')