from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta, timezone

class User(db.Model):
    __tablename__ = "users"
    id= db.Column (db.Integer, primary_key= True)
    email = db.Column( db.String(120), unique=True, nullable=False)
    password_hash = db.Column (db.String(200), nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)

    reset_token = db.Column (db.String(100), nullable=True)
    reset_token_expire = db.Column (db.DateTime, nullable=True)

    def __repr__ (self):
        return self.email
    
    @property
    def password (self):
        raise AttributeError ('password is not a readable attribute.')
    
    @password.setter
    def password (self, password):
        self.password_hash=generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)
    
    def generate_reset_token(self):
        self.reset_token= secrets.token_urlsafe(32)
        self.reset_token_expire= datetime.now()+ timedelta (minutes=30)
        return self.reset_token