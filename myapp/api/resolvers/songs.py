from ariadne import convert_kwargs_to_snake_case
from api import db
from ..models import Songs

@convert_kwargs_to_snake_case
def list_songs_resolver(obj,info):
    try:
        songs =  [song.to_dict() for song in Songs.query.all()]
        payload = {
            "success":True,
            "songs":[songs]
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def get_song_resolver(obj,info,id):
    try:
        song = Songs.query.get(id)
        payload = {
            "success": True,
            "song":song
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload

queries = {"listSongs":list_songs_resolver,"getSong":get_song_resolver}

mutations = {}

songs_resolver = {
    "queries":queries,
    "mutation":mutations
}