from . import db
from datetime import datetime, timezone

class ContactMessage(db.Model):
    __tablename__="contactmessage"
    id= db.Column (db.Integer, primary_key=True)
    message= db.Column (db.Text(1000),nullable=False)
    email= db.Column (db.String(120), nullable=False)
    created_time= db.Column (db.DateTime, default=datetime.now() ,nullable=False)

def __repr__ (self):
    return self.ContactMessage