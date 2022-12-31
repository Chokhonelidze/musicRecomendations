from api import app, db
from datetime import datetime
import pandas as pd

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

class Songs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    song_id = db.Column(db.Integer)
    play_count = db.Column(db.Integer)
    title = db.Column(db.String)
    release = db.Column(db.String)
    artist_name = db.Column(db.String)
    year = db.Column(db.Integer)
    def to_dict(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "song_id":self.song_id,
            "play_count":self.play_count,
            "title":self.title,
            "release":self.release,
            "artist_name":self.artist_name,
            "year":self.year
        }
with app.app_context():
    db.create_all()
    """
    filename="song_data.csv"
    data =pd.read_csv("/usr/local/src/webapp/src/api/"+filename)
    
    for index,row in data.iterrows():
        song = Songs(
            id=row[0],
            user_id = row[1],
            song_id = row[2],
            play_count = row[3],
            title = row[4],
            release = row[5],
            artist_name = row[6],
            year = row[7]
        )
        db.session.add(song)
    db.session.commit()
    """
   
