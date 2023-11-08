from . import movies
from flask import request, jsonify, session
from flask.views import MethodView
from ..models import db, Movie, User
from datetime import datetime
from sqlalchemy import asc, desc

class MovieListView(MethodView):
    def get(self):
        page = request.args.get('page', type=int, default=1)
        per_page = request.args.get('per_page', type=int, default=10)
        sort_by = request.args.get('sort_by', default='release_year')  # Default sorting by release_date
        sort_order = request.args.get('sort_order', default='asc')  # Default sorting order is ascending
        
        genre = request.args.get('genre')
        director = request.args.get('director')
        release_year = request.args.get('release_year')
        
        if release_year:
          release_year = str(release_year+"%")
        
        # building query based on the provided filters
        query = Movie.query
        
        if genre:
            query = query.filter(Movie.genre == genre)
        
        if director:
            query = query.filter(Movie.director == director)
        
        if release_year:
            query = query.filter(Movie.release_date.like(release_year))
        
        # Check if the sort_order is valid (asc or desc)
        if sort_order not in ('asc', 'desc'):
          return jsonify({"message": "Invalid sort_order, use 'asc' or 'desc'"}), 400

        # Define the sorting order (asc or desc) based on the sort_order parameter
        sort_order = asc if sort_order == 'asc' else desc

        # Determine which column to sort by based on the sort_by parameter
        if sort_by == 'release_year':
          sort_column = Movie.release_date
        elif sort_by == 'ticket_price':
          sort_column = Movie.ticket_price
        else:
          return jsonify({"message": "Invalid sort_by, use 'release_year' or 'ticket_price'"}), 400

        movies = query.order_by(sort_order(sort_column)).paginate(page=page, per_page=per_page, error_out=False)
        
        movie_list = [{"id": movie.id, "title": movie.title} for movie in movies.items]

        response = {
            'movies': movie_list,
            'total_movies': movies.total,
            'current_page': movies.page,
            'per_page': movies.per_page,
            'has_next': movies.has_next,
            'has_prev': movies.has_prev,
        }

        return jsonify(response)
    
    def post(self):
        if 'user_id' not in session:
            return jsonify({"message": "Login required"})
        data = request.get_json()
        data['creator_id'] = session['user_id']
        movie = Movie(**data)
        existing_movie = Movie.query.filter_by(title=movie.title).first()

        #validate movie title
        if existing_movie:
          response = {'message': 'movie already exists. Please choose a different one.'}
          return jsonify(response), 400
        
        #Validate movie release_date
        try:
         movie.release_date = datetime.strptime(movie.release_date, '%Y-%m-%d')
         if movie.release_date > datetime.now():
            return jsonify({"message":"Release date cannot be in the future"})
        except ValueError:
          return jsonify({"message":"Invalid release date format, use YYYY-MM-DD format"})

        # validate movie average rating
        if float(movie.average_rating) < 1 or float(movie.average_rating) > 10:
          return jsonify({"message":"Average rating must be between 1 and 10"})
        db.session.add(movie)
        db.session.commit()
        return jsonify({"message": "Movie created successfully"}), 200
    
class MovieDetailView(MethodView):
    def get(self, movie_id):
        movie = Movie.query.get(movie_id)
        
        #extract data from movies in dictionary
        if movie:
         movie_dict = {
            "id": movie.__dict__['id'],
            "title":movie.__dict__['title'],
            "description":movie.__dict__['description'],
            "release_date":movie.__dict__['release_date'],
            "director":movie.__dict__['director'],
            "genre":movie.__dict__['genre'],
            "average_rating":movie.__dict__['average_rating'],
            "ticket_price":movie.__dict__['ticket_price'],
            "cast":movie.__dict__['cast'],
            "creator_id":movie.__dict__['creator_id']
          }
         return jsonify(movie_dict)
        else:
            return jsonify({"message": "Movie not found"}), 404

    def put(self, movie_id):
        if 'user_id' not in session:
            return jsonify({"message": "Login required"}), 403
        
        movie = Movie.query.get(movie_id)

        if not movie:
            return jsonify({"message": "Movie not found"}), 404
        
        data = request.get_json()
        user = User.query.get(session['user_id'])

        #check if the user is the creator of the movie or is an admin
        if movie.__dict__['creator_id'] == session['user_id'] or user.__dict__['is_admin']:
          for key, value in data.items():
              setattr(movie, key, value)
          db.session.commit()
          return jsonify({"message": "Movie updated successfully"})
        else:
           return jsonify({"message":"You don't have authorization"}), 403

    def delete(self, movie_id):
        if 'user_id' not in session:
            return jsonify({"message": "Login required"}), 200
        movie = Movie.query.get(movie_id)
        user = User.query.get(session['user_id'])

        if not movie:
            return jsonify({"message": "Movie not found"}), 404
        
        if movie.__dict__['creator_id'] == session['user_id'] or user.__dict__['is_admin']:
          db.session.delete(movie)
          db.session.commit()
          return jsonify({"message": "Movie deleted successfully"})
        else:
           return jsonify({"message":"you are not authorized"}), 403
    

# Register the views with their URLs
movies.add_url_rule('/movies', view_func=MovieListView.as_view('movie_list'))
movies.add_url_rule('/movies/<int:movie_id>', view_func=MovieDetailView.as_view('movie_detail'))

    