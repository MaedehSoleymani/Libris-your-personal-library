from . import db
from sqlalchemy import Enum

class Book (db.Model):
    __tablename__= "books"

    id= db.Column (db.Integer, primary_key=True)
    title= db.Column (db.String(100), nullable=False)
    author= db.Column (db.String(100), nullable=False)
    pages= db.Column (db.Integer, nullable= False)
    genre= db.Column (Enum(
            'ادبیات کلاسیک',
            'فانتزی',
            'علمی‌تخیلی',
            'راز و رمز',
            'جنایی',
            'عاشقانه',
            'تاریخی',
            'زندگینامه',
            'خودیاری',
            'فانتزی تاریخی',
            'ترسناک',
            'ماجراجویی',
            'درام',
            'کودک',
            'نوجوان',
            'شعر',
            'نمایشنامه',
            'غیرداستانی',
            'فلسفه',
            'روانشناسی',
            'علمی',
            'تاریخ',
            'سیاسی',
            'اقتصادی',
            'مذهبی',
            'سفر',
            'آشپزی',
            'ورزشی',
            'هنر',
            'موسیقی',
            name="book_genre"
            ),
        nullable=False)
    status = db.Column(Enum(
            "خوانده نشده",
            "در حال مطالعه",
            "خوانده شده",
            name="book_status"
        ),
        nullable=False, default="خوانده نشده")
    rating = db.Column (db.Float, nullable=True)
    comment = db.Column (db.String (5000), nullable=True)

    user_id= db.Column (db.Integer, db.ForeignKey('users.id'), nullable=False)