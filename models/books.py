from . import db
from sqlalchemy import Enum

class Book (db.Model):
    __tablename__= "books"

    id= db.Column (db.Integer, primary_key=True)
    title= db.Column (db.String(100), nullable=False)
    author= db.Column (db.String(100), nullable=False)
    pages= db.Column (db.Integer, nullable= False)
    genre= db.Column (db.String(100), nullable=False)
    status = db.Column(Enum(
            "خوانده نشده",
            "در حال مطالعه",
            "خوانده شده",
            name="book_status"
        ),
        nullable=False, default="خوانده نشده")