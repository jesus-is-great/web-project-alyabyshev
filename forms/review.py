from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import SubmitField, SelectField, IntegerRangeField
from wtforms.validators import DataRequired, NumberRange


class ReviewForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField("Содержание", validators=[DataRequired()])
    submit = SubmitField('Применить', validators=[DataRequired()])
    film = SelectField('Фильм', default="", validators=[DataRequired()])
    rating = IntegerRangeField('Оценка', validators=[DataRequired(), NumberRange(min=0, max=10)])

    def edit_film(self, films):
        self.film.choices = sorted([(film.id, f"{film.name}({str(film.year)})") for film in films], key=lambda x: x[1])