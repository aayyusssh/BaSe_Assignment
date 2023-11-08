from . import user_rating
from flask import request, jsonify, session
from flask.views import MethodView
from ..models import db, Movie, UserRating


class UserRatingView(MethodView):
    def post(self, movie_id):
        if 'user_id' not in session:
            return jsonify({"message":"Login first"})
        
        data = request.get_json()
        user_id = session['user_id']
        movie_id = int(movie_id)
        rating = data.get('rating')

        if float(rating) < 1 or float(rating) > 10:
          return jsonify({"message":"Rating must be between 1 and 10"})
        
        #check if the user has already reviewed the movie
        existing_review = UserRating.query.filter_by(user_id=user_id,movie_id=movie_id).first()

        if existing_review:
            setattr(existing_review, 'rating', rating)
            db.session.commit()
            return jsonify({"message": "Movie rating updated successfully"})
        
        # Create a new UserRating entry
        user_rating = UserRating(user_id=user_id, movie_id=movie_id, rating=rating)
        db.session.add(user_rating)
        db.session.commit()

        return jsonify({"message": "Rating added successfully"}), 201

class MovieRatingsView(MethodView):
    def get(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            ratings = UserRating.query.filter_by(movie_id=movie.id).all()
            rating_list = [{"user_id": rating.user_id, "rating": rating.rating} for rating in ratings]
            return jsonify({"movie_id": movie.__dict__["id"], "ratings": rating_list})
        return jsonify({"message": "Movie not found"}), 404
    
# Register the views with their URLs
user_rating.add_url_rule('/movies/user_rating/<int:movie_id>', view_func=UserRatingView.as_view('user_rating'))
user_rating.add_url_rule('/movies/movie_ratings/<int:movie_id>', view_func=MovieRatingsView.as_view('movie_ratings'))