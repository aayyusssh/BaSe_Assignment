from ..models import Movie
from . import search
from flask import request, jsonify
from sqlalchemy import or_

@search.route('/search/movies', methods=['GET'])
def search_movies():
    search_term = request.args.get('q')

    if not search_term:
        return jsonify({"message": "Search term is required"}), 400

    # Perform the search using the 'ilike' method to make it case-insensitive
    movies = Movie.query.filter(
        or_(
            Movie.title.ilike(f"%{search_term}%"),
            Movie.description.ilike(f"%{search_term}%"),
            Movie.genre.ilike(f"%{search_term}%"),
            Movie.cast.ilike(f"%{search_term}%")
        )
    ).all()

    movie_list = [{"id": movie.id, "title": movie.title} for movie in movies]

    return jsonify(movie_list), 200