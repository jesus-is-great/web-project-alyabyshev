from flask import Flask, render_template, redirect, request, abort
from data import db_session, review_resources
from data.films import Film
from data.reviews import Review
from data.users import User
from data.genres import Genre
from forms.user import RegisterForm, LoginForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from forms.review import ReviewForm
from forms.film import FilmForm
from forms.review_by_film import ReviewFromFilmForm
from forms.search_film import SearchFilmForm
from flask_restful import abort, Api


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
api.add_resource(review_resources.ReviewsListResource, '/api/v2/news')
api.add_resource(review_resources.ReviewResource, '/api/v2/news/<int:news_id>')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    db_sess = db_session.create_session()
    reviews = db_sess.query(Review).order_by(Review.created_date.desc())
    return render_template('index.html', reviews=reviews)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/review', methods=['GET', 'POST'])
@login_required
def add_review():
    form = ReviewForm()
    db_sess = db_session.create_session()
    films = db_sess.query(Film).all()
    form.edit_film(films)
    db_sess.commit()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        review = Review()
        review.title = form.title.data
        review.content = form.content.data
        review.rating = form.rating.data
        film = db_sess.query(Film).filter(Film.id == form.film.data).first()
        review.film_id = film.id
        current_user.reviews.append(review)
        db_sess.merge(current_user)
        db_sess.query(Film).filter(Film.id == review.film_id).first().update_rating()
        db_sess.commit()
        return redirect('/')
    return render_template('review.html', title='Добавление записи',
                           form=form)


@app.route('/review/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_review(id):
    form = ReviewForm()
    db_sess = db_session.create_session()
    films = db_sess.query(Film).all()
    form.edit_film(films)
    db_sess.commit()
    if request.method == "GET":
        db_sess = db_session.create_session()
        review = db_sess.query(Review).filter(Review.id == id,
                                              Review.user == current_user
                                              ).first()
        if review:
            form.title.data = review.title
            form.content.data = review.content
            form.film.data = review.film_id
            form.rating.data = review.rating
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        review = db_sess.query(Review).filter(Review.id == id,
                                              Review.user == current_user
                                              ).first()
        if review:
            review.title = form.title.data
            review.content = form.content.data
            review.film_id = form.film.data
            review.rating = form.rating.data
            db_sess.query(Film).filter(Film.id == review.film_id).first().update_rating()
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('review.html',
                           title='Редактирование записи',
                           form=form
                           )


@app.route('/review_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def review_delete(id):
    db_sess = db_session.create_session()
    review = db_sess.query(Review).filter(Review.id == id,
                                          Review.user == current_user
                                          ).first()
    if review:
        db_sess.delete(review)
        db_sess.query(Film).filter(Film.id == review.film_id).first().update_rating()
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/film", methods=['GET', 'POST'])
@login_required
def add_film():
    form = FilmForm()
    db_sess = db_session.create_session()
    genres = db_sess.query(Genre).all()
    form.edit_genres(genres)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        film = Film()
        film.name = form.name.data
        film.year = form.year.data
        film.director = form.director.data
        for id in form.genres.data:
            film.genres.append(db_sess.query(Genre).filter(Genre.id == id).first())
        db_sess.add(film)
        db_sess.commit()
        return redirect('/film/' + str(film.id))
    return render_template('add_film.html', title='Добавление фильма',
                           form=form)


@app.route("/film/<int:id>", methods=['GET', 'POST'])
def film(id):
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    return render_template('film.html', film=film)


@app.route('/review_by_film/<int:id>', methods=['GET', 'POST'])
@login_required
def review_by_film(id):
    form = ReviewFromFilmForm()
    db_sess = db_session.create_session()
    film = db_sess.query(Film).filter(Film.id == id).first()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        film = db_sess.query(Film).filter(Film.id == id).first()
        review = Review()
        review.title = form.title.data
        review.content = form.content.data
        review.rating = form.rating.data
        review.film_id = id
        current_user.reviews.append(review)
        db_sess.merge(current_user)
        film.update_rating()
        db_sess.commit()
        return redirect('/')
    return render_template('review_by_film.html', title='Добавление записи',
                           form=form, film=film.name)


@app.route('/search', methods=['GET', 'POST'])
def search_film():
    form = SearchFilmForm()
    db_sess = db_session.create_session()
    films = db_sess.query(Film).all()
    form.edit_film(films)
    db_sess.commit()
    if form.validate_on_submit():
        return redirect('/film/' + str(form.film.data))
    return render_template('search_film.html', title='Поиск фильма', form=form)


def main():
    db_session.global_init("db/reviews.db")
    app.run()


if __name__ == '__main__':
    main()
