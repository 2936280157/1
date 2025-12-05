# models.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default="reader")  # reader / author / admin
    display_author_ui = db.Column(db.Boolean, default=False)

    author_profile = db.relationship("Author", backref="user", uselist=False)

    def is_admin(self):
        return self.role == "admin"

    def is_author(self):
        return self.role == "author"


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pen_name = db.Column(db.String(80), nullable=False)

    # ✅ 新增：作者专栏名字（可为空）
    column_name = db.Column(db.String(120), nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    books = db.relationship("Book", backref="author", lazy=True, cascade="all, delete-orphan")
    albums = db.relationship("Album", backref="author", lazy=True, cascade="all, delete-orphan")


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    chapters = db.relationship("Chapter", backref="book", lazy=True, cascade="all, delete-orphan")
    notes = db.relationship("Note", backref="book", lazy=True, cascade="all, delete-orphan")


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=True)

    order_index = db.Column(db.Integer, default=1)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)


class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    notes = db.relationship("Note", backref="album", lazy=True, cascade="all, delete-orphan")
    visit_logs = db.relationship("VisitLog", backref="album", lazy=True, cascade="all, delete-orphan")


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=True)
    album_id = db.Column(db.Integer, db.ForeignKey("album.id"), nullable=True)


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)

    user = db.relationship("User", backref=db.backref("favorites", lazy=True))
    book = db.relationship("Book", backref=db.backref("favorites", lazy=True))


class VisitLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime, default=datetime.utcnow)

    album_id = db.Column(db.Integer, db.ForeignKey("album.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    user = db.relationship("User", backref=db.backref("visit_logs", lazy=True))
