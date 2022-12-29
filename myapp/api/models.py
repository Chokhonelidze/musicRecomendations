from api import app, db
from datetime import datetime
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.String)
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": datetime.now()
        }
with app.app_context():
    db.create_all()

class User(db.Model): 
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.String)
    def to_dict(self):
        return {
            "id":self.id,
            "email":self.email,
            "password":self.password,
            "role":self.role,
            "created_at":datetime.now()
        }
with app.app_context():
    db.create_all()