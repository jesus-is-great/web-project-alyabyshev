from flask import jsonify
from . import db_session
from .reviews import Review
from .films import Film
from flask_restful import reqparse, Resource, abort


def abort_if_review_not_found(review_id):
    session = db_session.create_session()
    review = session.query(Review).get(review_id)
    if not review:
        abort(404, message=f"Review {review_id} not found")


class ReviewResource(Resource):
    def get(self, review_id):
        abort_if_review_not_found(review_id)
        session = db_session.create_session()
        review = session.query(Review).get(review_id)
        return jsonify({'review': review.to_dict(
            only=('film_id', 'rating', 'title', 'content', 'user_id'))})

    def delete(self, review_id):
        abort_if_review_not_found(review_id)
        session = db_session.create_session()
        review = session.query(Review).get(review_id)
        film = session.query(Film).filter(Film.id == review.film_id).first()
        session.delete(review)
        film.update_rating()
        session.commit()
        return jsonify({'success': 'OK'})


class ReviewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        review = session.query(Review).all()
        return jsonify({'review': [item.to_dict(
            only=('film_id', 'rating', 'title', 'content', 'user_id')) for item in review]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        review = Review(
            film_id=args['film_id'],
            rating=args['rating'],
            title=args['title'],
            content=args['content'],
            user_id=args['user_id'],
        )
        session.add(review)
        session.query(Film).filter(Film.id == args['film_id']).first().update_rating()
        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('film_id', required=True, type=int)
parser.add_argument('rating', required=True, type=int)
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)