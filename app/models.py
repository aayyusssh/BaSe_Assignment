from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#user rating model
class UserRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

#movies model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    release_date = db.Column(db.String(10))
    director = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    average_rating = db.Column(db.Float)
    ticket_price = db.Column(db.Float)
    cast = db.Column(db.String(500))
    creator_id = db.Column(db.Integer, nullable=False)
    ratings = db.relationship('UserRating', backref='movie', lazy=True)

#user model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)



