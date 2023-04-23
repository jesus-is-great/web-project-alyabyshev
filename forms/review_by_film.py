from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField, IntegerRangeField
from wtforms.validators import DataRequired, NumberRange


class ReviewFromFilmForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    submit = SubmitField('Применить', validators=[DataRequired()])
    rating = IntegerRangeField('Оценка', validators=[DataRequired(), NumberRange(min=0, max=10)])