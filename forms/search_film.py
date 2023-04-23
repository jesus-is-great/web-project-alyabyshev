from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired


class SearchFilmForm(FlaskForm):
    film = SelectField("Поиск по фильмам")
    submit = SubmitField('Найти', validators=[DataRequired()])

    def edit_film(self, films):
        self.film.choices = sorted([(film.id, f"{film.name}({str(film.year)})") for film in films], key=lambda x: x[1])