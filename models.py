from flask_sqlalchemy import SQLAlchemy
# OOP-Klassen (User & Movie)
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    def __str__(self):
        return f"User(id={self.id}, name={self.name})"

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    director = db.Column(db.String(100))
    year = db.Column(db.Integer)
    poster_url = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('movies', lazy=True, cascade='all, delete-orphan'))
    def __str__(self):
        return f"Movie(id={self.id}, title={self.title})"
