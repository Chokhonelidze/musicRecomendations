from api import app, db
from datetime import datetime
import pandas as pd
from datetime import date

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
    link = db.Column(db.String)
    def to_dict(self):
        return {
            "id":self.id,
            "user_id":self.user_id,
            "song_id":self.song_id,
            "play_count":self.play_count,
            "title":self.title,
            "release":self.release,
            "artist_name":self.artist_name,
            "link":self.link,
            "year":self.year
        }
with app.app_context():
    db.create_all()
    print(Songs.query.first())
    if not Songs.query.first():
        filename="final_data.csv"
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
            today = date.today()
            email = str(row[1])+"@yahoo.com";
            userf = User.query.filter_by(email=email).first()
            if not userf:
                userI = User(
                    id = row[1],
                    email=email,
                    password="123456",
                    role=0,
                    created_at=today.strftime("%Y-%m-%d %H:%M:%S")
                    )
                db.session.add(userI)

            db.session.add(song)
        db.session.commit()
    