from ..models import Songs,Song,Downlods
from ariadne import convert_kwargs_to_snake_case
from pytube import YouTube
import os
from api import db,executor
import re
from api.core.functions.saveText import get_throttling_function_name,saveText
from api.core.functions.searchText import getSongs,deleteSongs,restChroma,loadDataToChroma
@convert_kwargs_to_snake_case
def searchSong(obj,info,song_text,model):
    try:
        #deleteSongs(["202","605","703","4"])
        data = getSongs(songText=song_text,model=model)
     

        # song = Song.query.filter(Song.song_id == '6222').first()
        # saveText(song.link,str(song.song_id))
        return data
    except Exception as error:
        print(error)
    return []

def resetChroma(obj,info,name):
    try:
        restChroma(name)
        return "ok"
    except Exception as error:
        return (error)
    

def retrainChroma(obj,info,name,chank,overlap):
    try:
        loadDataToChroma(name,chank,overlap)
        return "ok"
    except Exception as e:
        return e
        

@convert_kwargs_to_snake_case
def list_songs_resolver(obj,info,filters=None):
    try:
        if filters.get("search"):
            if filters.get("filter") == 'AI':
                ai_search = getSongs(songText=filters.get("search"),model="nomic-ai/nomic-embed-text-v1")
                songs = [song.to_dict() for song in Song.query.filter(Song.song_id.in_(ai_search)).all()]
            elif filters['filter'] == 'title':
                songs =  [song.to_dict() for song in Song.query.filter((Song.title.ilike("%"+filters['search']+"%"))).limit(filters['limit']).offset(filters['offset']).all()]
            elif filters['filter'] == 'release':
                songs =  [song.to_dict() for song in Song.query.filter((Song.release.ilike("%"+filters['search']+"%"))).limit(filters['limit']).offset(filters['offset']).all()]
            elif filters['filter'] == 'artist_name':
                songs =  [song.to_dict() for song in Song.query.filter((Song.artist_name.ilike("%"+filters['search']+"%"))).limit(filters['limit']).offset(filters['offset']).all()]
            elif filters['filter'] == 'year':
                songs =  [song.to_dict() for song in Song.query.filter_by(year=filters['search']).limit(filters['limit']).offset(filters['offset']).all()]

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

@convert_kwargs_to_snake_case
def download_song_resolver(obj,info,link):
    try:
        # cipher.get_throttling_function_name = get_throttling_function_name
        # ty = YouTube(str(link))
        # video = ty.streams.filter(only_audio=True).first()
        # destination = "/downloads/"
        # out_file = video.download(output_path=destination)
        # base, ext = os.path.splitext(out_file)
        # new_file = base + '.mp3'
        # os.rename(out_file, new_file)
       
        # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        # len(encoding.encode(transcript))
        #saveText(link,"202")
        return "new_file"
    except Exception as error:
        print("error=",error,flush=True)

@convert_kwargs_to_snake_case
def update_song_resolver(obj,info,song):
    try:
        assert(song.get('id'))
        songI = Song.query.get(song.get('id'))
        assert(songI)
        if song.get('title'):
            setattr(songI,"title",song.get('title'));
        if(song.get('release')):
            #songI['release'] = song.get('release')
            setattr(songI,"release",song.get('release'));
        if(song.get('artist_name')):
            #songI['artist_name'] = song.get('artist_name')
            setattr(songI,"artist_name",song.get('artist_name'));
        if(song.get('link')):
            #songI['link'] = song.get('link')
            setattr(songI,"link",song.get('link'));
        if(song.get('year')):
            #songI['year'] = song.get('year')
            setattr(songI,"year",song.get('year'));      
        db.session.commit()
        payload = {
            "success":True,
            "song":songI
        }
    except Exception as error:
        payload = {
            "success":False,
            "errors":[str(error)]
        }
    return payload


mutations = {
    "createNewPureSong":create_song_resolver,
    "updatePureSong":update_song_resolver
}
queries = {
    "listPureSongs":list_songs_resolver,
    "downloadSong":download_song_resolver,
    "searchSong":searchSong,
    "retrainChroma":retrainChroma,
    "resetChroma":resetChroma
}
pure_songs_resolver = {
    "queries":queries,
    "mutations":mutations
}