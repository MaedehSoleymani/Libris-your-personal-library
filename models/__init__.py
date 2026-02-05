from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .users import User
from .books import Book