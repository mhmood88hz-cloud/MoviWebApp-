from models import db, User, Movie
from sqlalchemy.exc import SQLAlchemyError

class DataManager:
    def create_user(self, name: str) -> User:
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during user creation: {e}")
            return None
    def get_users(self):
        try:
            return User.query.all()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []
    def get_movies(self, user_id: int):
        try:
            return Movie.query.all()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []
    def add_movie(self, movie):
        try:
            db.session.add(movie)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error: {e}")
            return False
    def update_movie(self, movie_id, new_title):
        try:
            movie = Movie.query.get(movie_id)
            if movie:
                movie.title = new_title
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error: {e}")
            return False
    def delete_movie(self, movie_id):
        try:
            movie = Movie.query.get(movie_id)
            if movie:
                db.session.delete(movie)
                db.session.commit()
                return True
            return False
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error: {e}")
            return False
