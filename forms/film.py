from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField, SelectMultipleField, IntegerField, FileField
from wtforms.validators import DataRequired


class FilmForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    year = IntegerField("Год", validators=[DataRequired()])
    director = StringField("Режиссер", validators=[DataRequired()])
    submit = SubmitField('Применить', validators=[DataRequired()])
    genres = SelectMultipleField('Жанры', coerce=int, validators=[DataRequired()])
    file = FileField('Обложка', validators=[DataRequired()])

    def edit_genres(self, genres):
        self.genres.choices = sorted([(genre.id, genre.genre) for genre in genres], key=lambda x: x[1])