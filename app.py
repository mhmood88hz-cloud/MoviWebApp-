import os
from typing import Union
import requests
from flask import Flask, render_template, request, redirect, url_for, Response
from data_manager import DataManager
from models import db, Movie, User
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data/movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

data_manager = DataManager()
OMDB_API_KEY = os.getenv('OMDB_API_KEY', 'fallback_key')


@app.route('/')
def index() -> str:
    """Renders the main dashboard page displaying a grid of all registered users."""
    users = data_manager.get_users()
    return render_template('index.html', users=users)


@app.route('/users', methods=['POST'])
def create_user() -> Response:
    """Handles the creation of a new user via POST form submission and redirects home."""
    username = request.form.get('user_name')
    if username:
        data_manager.create_user(name=username)
    return redirect(url_for('index'))


@app.route('/users/<int:user_id>/movies', methods=['GET'])
def list_user_movies(user_id: int) -> str:
    """Displays the personalized favorite movies list page for a specific user ID."""
    actual_user = User.query.get_or_404(user_id)
    filme = data_manager.get_movies(user_id)
    return render_template('movies.html', user=actual_user, movies=filme)


@app.route('/users/<int:user_id>/movies', methods=['POST'])
def add_movie_to_user(user_id: int) -> Response:
    """Fetches movie data from OMDb API by title, saves it to the user, and redirects."""
    movie_title = request.form.get('movie_title')
    if movie_title:
        try:
            url = f'http://omdbapi.com{OMDB_API_KEY}&t={movie_title}'
            response = requests.get(url, timeout=5).json()
            if response.get('Response') == 'True':
                title = response.get('Title')
                year = response.get('Year')
                year_clean = int(''.join(filter(str.isdigit, year))) if year else 2000
                director = response.get('Director')
                poster = response.get('Poster')
            else:
                raise ValueError('Movie not found in OMDB')
        except (requests.RequestException, ValueError):
            title = movie_title
            year_clean = 2000
            director = 'Unknown'
            poster = 'https://placeholder.com'

        new_movie = Movie(title=title, year=year_clean, director=director, poster_url=poster, user_id=user_id)
        data_manager.add_movie(new_movie)
    return redirect(url_for('list_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_user_movie(user_id: int, movie_id: int) -> Response:
    """Updates the title of a specific movie item and redirects back to the movie list."""
    neuer_titel = request.form.get('new_title')
    if neuer_titel:
        data_manager.update_movie(movie_id, new_title=neuer_titel)
    return redirect(url_for('list_user_movies', user_id=user_id))


@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_user_movie(user_id: int, movie_id: int) -> Response:
    """Deletes a specific movie entry from the database and updates the view."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for('list_user_movies', user_id=user_id))


with app.app_context():
    if not os.path.exists('data'):
        os.makedirs('data')
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
