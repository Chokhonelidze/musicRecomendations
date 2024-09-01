from ..models import Song
from ariadne import convert_kwargs_to_snake_case
from pytube import YouTube
import os
from api import db
from pytube.innertube import _default_clients
from pytube import cipher
import re

@convert_kwargs_to_snake_case
def list_songs_resolver(obj,info,filters=None):
    try:
        if filters.get("search"):
            if filters['filter'] == 'title':
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


_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]

def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    #logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            #logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )




@convert_kwargs_to_snake_case
def download_song_resolver(obj,info,link):
    try:
        cipher.get_throttling_function_name = get_throttling_function_name
        ty = YouTube(str(link))
        video = ty.streams.filter(only_audio=True).first()
        destination = "/downloads/"
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return new_file
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
    "downloadSong":download_song_resolver
}
pure_songs_resolver = {
    "queries":queries,
    "mutations":mutations
}