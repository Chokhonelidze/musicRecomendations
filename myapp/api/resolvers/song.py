from ..models import Song
from ariadne import convert_kwargs_to_snake_case
from api import db

@convert_kwargs_to_snake_case
def list_songs_resolver(obj,info,filters=None):
    try:
        if filters.get('user'):
            songs = [song.to_dict() for song in Song.query.limit(filters['limit']).offset(filters['offset']).all()];
        elif filters.get("search"):
            if filters['filter'] == 'title':
                songs =  [song.to_dict() for song in Song.query.filter((Song.title.like("%"+filters['search']+"%"))).limit(filters['limit']).offset(filters['offset']).all()]
            elif filters['filter'] == 'release':
                songs =  [song.to_dict() for song in Song.query.filter((Song.release.like("%"+filters['search']+"%"))).limit(filters['limit']).offset(filters['offset']).all()]
            elif filters['filter'] == 'artist_name':
                songs =  [song.to_dict() for song in Song.query.filter((Song.artist_name.like("%"+filters['search']+"%"))).limit(filters['limit']).offset(filters['offset']).all()]
            elif filters['filter'] == 'year':
                songs =  [song.to_dict() for song in Song.query.filter((Song.year.like("%"+filters['search']+"%"))).limit(filters['limit']).offset(filters['offset']).all()]

        else:
             songs =  [song.to_dict() for song in Song.query.limit(filters['limit']).offset(filters['offset']).all()] 
        payload = {
            "success":True,
            "songs":songs
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def create_song_resolver(obj,info,song):
    try:
        songI = Song(
            title = song['title'],
            release = song['release'],
            artist_name = song['artist_name'],
            link = song['link'],
            year = song['year'] 
        )
        db.session.add(songI)
        db.session.commit()
        payload = {
            "success": True,
            "song": songI.to_dict()
        }
    except Exception as error:
        payload = {
            "success":False,
            "errors":[str(error)]
        }
    return payload

mutations = {
    "createPureSong":create_song_resolver,
}
queries = {
    "listPureSongs":list_songs_resolver,
}
pure_songs_resolver = {
    "queries":queries,
    "mutations":mutations
}