import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('films', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('films.id')),
    sqlalchemy.Column('genres', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('genres.id'))
)


class Genre(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'genres'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    genre = sqlalchemy.Column(sqlalchemy.String)