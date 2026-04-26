from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    price = IntegerField("Цена", validators=[DataRequired()])
    content = HiddenField("Описание")
    tags = TextAreaField("Теги", validators=[DataRequired()])
    image = StringField('URL картинки', validators=[DataRequired()])
    submit = SubmitField('Опубликовать')