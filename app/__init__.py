from flask import Flask
from app.auth import auth
from app.movies import movies
from app.search import search
from app.user_rating import user_rating
from .models import db
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.json'  # Our API url (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Movies API"
    },
    
)

#every blueprints
app.register_blueprint(swaggerui_blueprint)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(movies, url_prefix='/api')
app.register_blueprint(search, url_prefix='/api')
app.register_blueprint(user_rating, url_prefix='/api')

app.secret_key = 'your_secret_key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
app.app_context().push()


db.init_app(app)
db.create_all()  