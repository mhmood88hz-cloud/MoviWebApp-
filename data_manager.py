from typing import List, Optional
from models import db, User, Movie
from sqlalchemy.exc import SQLAlchemyError


class DataManager:
    """Manages all CRUD operations for the application database using SQLAlchemy ORM."""

    def create_user(self, name: str) -> Optional[User]:
        """Creates a new user entry in the database.

        Args:
            name (str): The username of the new user.

        Returns:
            Optional[User]: The created User object, or None if a database error occurs.
        """
        try:
            new_user = User(name=name)
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error during user creation: {e}")
            return None

    def get_users(self) -> List[User]:
        """Retrieves a list of all registered users from the database.

        Returns:
            List[User]: A list containing all User objects.
        """
        try:
            return User.query.all()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []

    def get_movies(self, user_id: int) -> List[Movie]:
        """Retrieves all favorite movies belonging to a specific user.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            List[Movie]: A list of Movie objects linked to the user.
        """
        try:
            return Movie.query.filter_by(user_id=user_id).all()
        except SQLAlchemyError as e:
            print(f"Database error: {e}")
            return []

    def add_movie(self, movie: Movie) -> bool:
        """Adds a prepared Movie object to the user's favorites in the database.

        Args:
            movie (Movie): The Movie instance to be stored.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            db.session.add(movie)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"Database error: {e}")
            return False

    def update_movie(self, movie_id: int, new_title: str) -> bool:
        """Updates the title of an existing movie in the database.

        Args:
            movie_id (int): The unique ID of the movie.
            new_title (str): The updated movie title.

        Returns:
            bool: True if the update succeeded, False if the movie was not found or failed.
        """
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

    def delete_movie(self, movie_id: int) -> bool:
        """Deletes a movie from the database by its ID.

        Args:
            movie_id (int): The unique ID of the movie to delete.

        Returns:
            bool: True if deletion succeeded, False otherwise.
        """
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
