from api import app, db
from datetime import datetime
import pandas as pd
from datetime import date
from passlib.hash import sha256_crypt

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(1000))
    description = db.Column(db.String(2000))
    created_at = db.Column(db.String(200))
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
    email = db.Column(db.String(200))
    password = db.Column(db.String(300))
    role = db.Column(db.String(200))
    created_at = db.Column(db.String(200))
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

class Song(db.Model):
    song_id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(1000))
    release = db.Column(db.String(300))
    artist_name = db.Column(db.String(300))
    year = db.Column(db.Integer)
    link = db.Column(db.String(1000))
    def to_dict(self):
        return {
            "song_id":self.song_id,
            "title":self.title,
            "release":self.release,
            "artist_name":self.artist_name,
            "year":self.year,
            "link":self.link
        }
with app.app_context():
    db.create_all()

class Songs(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    song_id = db.Column(db.Integer)
    play_count = db.Column(db.Integer)
    title = db.Column(db.String(1000))
    release = db.Column(db.String(300))
    artist_name = db.Column(db.String(300))
    year = db.Column(db.Integer)
    link = db.Column(db.String(1000))
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
        data =pd.read_csv("/usr/local/src/webapp/api/"+filename)
        count = 0
        for index,row in data.iterrows():
            count+=1
            print(str(count))
            songs = Songs(
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
                    password=sha256_crypt.encrypt("123456"),
                    role=0,
                    created_at=today.strftime("%Y-%m-%d %H:%M:%S")
                    )
                db.session.add(userI)
            fsong = Song.query.get(row[2])
            if not fsong:
                fsong = Song(
                    song_id = row[2],
                    title = row[4],
                    release = row[5],
                    artist_name = row[6],
                    year = row[7]
                    )
                db.session.add(fsong)
            db.session.add(songs)
        db.session.commit()
    