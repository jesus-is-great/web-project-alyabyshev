import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from statistics import mean


class Film(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'films'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    year = sqlalchemy.Column(sqlalchemy.Integer)
    director = sqlalchemy.Column(sqlalchemy.String)
    rating = sqlalchemy.Column(sqlalchemy.Float, nullable=True, default=None)
    reviews = orm.relationship('Review', back_populates='film')
    genres = orm.relationship("Genre",
                                  secondary="association",
                                  backref="film")
    cover = sqlalchemy.Column(sqlalchemy.Boolean)

    def update_rating(self):
        if len(self.reviews) == 0:
            self.rating = None
        else:
            self.rating = mean([rev.rating for rev in self.reviews])