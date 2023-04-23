from data import db_session
from data.genres import Genre

db_session.global_init("db/reviews.db")


with open("genres.txt", "r", encoding='utf-8') as f:
    data = f.read().lstrip('\ufeff').split('\n')
db_sess = db_session.create_session()
for l in data:
    genre = Genre()
    genre.genre = l
    g = db_sess.query(Genre).filter(Genre.genre == l).first()
    if g is None:
        db_sess.add(genre)
db_sess.commit()