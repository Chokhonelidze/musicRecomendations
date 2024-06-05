from ariadne import convert_kwargs_to_snake_case
from api import db
from ..models import Songs,Song
from surprise.reader import Reader
from sqlalchemy import text,desc
from surprise.dataset import Dataset
from surprise.prediction_algorithms.knns import KNNBasic
import pandas as pd

def get_recommendations(data, user_id, top_n, algo):
    # Creating an empty list to store the recommended product ids
    recommendations = []
    
    # Creating an user item interactions matrix 
    user_item_interactions_matrix =  data.pivot(index='user_id', columns='song_id', values='play_count')
    
    # Extracting those business ids which the user_id has not visited yet
    non_interacted_products = user_item_interactions_matrix.loc[user_id][user_item_interactions_matrix.loc[user_id].isnull()].index.tolist()
    
    # Looping through each of the business ids which user_id has not interacted yet
    for item_id in non_interacted_products:
        
        # Predicting the ratings for those non visited restaurant ids by this user
        est = algo.predict(user_id,item_id).est

        # Appending the predicted ratings
        recommendations.append({"id":item_id,"score":est})

    # Sorting the predicted ratings in descending order
    recommendations.sort(key = lambda x : x["score"], reverse = True)

    return recommendations[:top_n] # Returing top n highest predicted rating products for this user
@convert_kwargs_to_snake_case
def predict_songs_resolver(obj,info,query):
    try:
        
        gs_optimized = KNNBasic(sim_options={'name':'pearson_baseline','user_based': True}, k=30, min_k=5, verbose=False)
        gs_optimized_item = KNNBasic(sim_options={'name':'pearson_baseline','user_based': False},random_state = 1, k=30, min_k=5, verbose=False)

        df = pd.read_sql_table('songs',db.get_engine(),index_col='id')
        #df = pd.read_json(df,dtype=False)
        print(df.head())
        #df = pd.read_csv('final_data.csv')
        reader = Reader(rating_scale=(0,5))
        data = Dataset.load_from_df(df[['user_id', 'song_id', 'play_count']], reader) 
        trainset = data.build_full_trainset()
        gs_optimized.fit(trainset)
        gs_optimized_item.fit(trainset)
        #p_play_count_play = gs_optimized.predict(query['user_id'],query["song_id"],verbose=True)
        #print(p_play_count_play)
        df_rating=df.drop_duplicates()
        recommendations =get_recommendations(df_rating,int(query.get("user_id")),3,gs_optimized)
        recommendations2 =get_recommendations(df_rating,int(query.get("user_id")),3,gs_optimized_item)
        frecommendations = recommendations + recommendations2
        
        obj = {}
        for song in frecommendations:
            if song["id"] in obj:
                obj[song["id"]]['common'] = True
            else:
                obj[song["id"]] = {
                    "score":song['score'],
                    "common": False
                }
        print(obj)
      
        finalfrecommendations = []
        for k in obj.keys():
            finalfrecommendations.append({"id":k,"score":obj[k]["score"],"common":obj[k]["common"]})
        print(finalfrecommendations)
        payload = {
            "success":True,
            "predict":finalfrecommendations
        }
    except Exception as error:
        print(error)
        payload = {
            "success":False,
            "errors":[str(error)]
        }
    return payload

    
@convert_kwargs_to_snake_case
def list_songs_resolver(obj,info,filters=None):
    try:
        if filters.get('user'):
            if(filters.get("search")):
                if filters['filter'] == 'title':
                    songs =  [song.to_dict() for song in Songs.query.filter((Songs.user_id == filters['user']) & (Songs.title.ilike("%"+filters['search']+"%"))).group_by(Songs.song_id,Songs.id).limit(filters['limit']).offset(filters['offset']).all()]
                elif filters['filter'] == 'release':
                    songs =  [song.to_dict() for song in Songs.query.filter((Songs.user_id == filters['user']) & (Songs.release.ilike("%"+filters['search']+"%"))).group_by(Songs.song_id,Songs.id).limit(filters['limit']).offset(filters['offset']).all()]
                elif filters['filter'] == 'artist_name':
                    songs =  [song.to_dict() for song in Songs.query.filter((Songs.user_id == filters['user']) & (Songs.artist_name.ilike("%"+filters['search']+"%"))).group_by(Songs.song_id,Songs.id).limit(filters['limit']).offset(filters['offset']).all()]
                elif filters['filter'] == 'year':
                    songs =  [song.to_dict() for song in Songs.query.filter((Songs.user_id == filters['user']) & (Songs.year == filters['search'])).group_by(Songs.song_id,Songs.id).limit(filters['limit']).offset(filters['offset']).all()]
            else:
                songs = [song.to_dict() for song in Songs.query.filter_by(user_id =filters['user']).order_by(desc(Songs.play_count)).limit(filters['limit']).offset(filters['offset']).all()];
        elif filters.get("search"):
            if filters['filter'] == 'title':
                songs =  [song.to_dict() for song in Songs.query.filter((Songs.title.ilike("%"+filters['search']+"%")) & (Songs.user_id != filters['user'])).group_by('song_id').limit(filters['limit']).offset(filters['offset']).all()]
            elif filters['filter'] == 'release':
                songs =  [song.to_dict() for song in Songs.query.filter((Songs.release.ilike("%"+filters['search']+"%")) & (Songs.user_id != filters['user'])).group_by('song_id').limit(filters['limit']).offset(filters['offset']).all()]
            elif filters['filter'] == 'artist_name':
                songs =  [song.to_dict() for song in Songs.query.filter((Songs.artist_name.ilike("%"+filters['search']+"%")) & (Songs.user_id != filters['user'])).group_by('song_id').limit(filters['limit']).offset(filters['offset']).all()]
            elif filters['filter'] == 'year':
                songs =  [song.to_dict() for song in Songs.query.filter_by( (Songs.year==filters['search']) & (Songs.user_id != filters['user'])).group_by('song_id').limit(filters['limit']).offset(filters['offset']).all()]

        else:
             songs =  [song.to_dict() for song in Songs.query.group_by('song_id').limit(filters['limit']).offset(filters['offset']).all()] 
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
def get_song_resolver(obj,info,id):
    try:
        song = Songs.query.filter_by(song_id=id).first()
        print(song)
        if song:
            song = song.to_dict()
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

queries = {"listSongs":list_songs_resolver,
            "getSong":get_song_resolver,
            "predictSong":predict_songs_resolver
            }

@convert_kwargs_to_snake_case
def create_song_resolver(obj,info,song):
    try:
        songf = Songs.query.filter((Songs.user_id  == song['user_id']) & (Songs.song_id == song['song_id'])).first();
        if not songf:
            songI = Songs(
                user_id = song['user_id'],
                song_id = song['song_id'],
                play_count = song['play_count'],
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
        else:
            payload = {
                "success":False,
                "errors":["user already has song"]
            }
    except Exception as error:
        payload = {
            "success":False,
            "errors":[str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def update_song_links(obj,info,song): 
    try:
        assert(song.get('id'))
        assert(song.get('link'))
        songs = Songs.query.filter_by(song_id=song.get('id')).all()
        ids = []
        for s in songs:
            setattr(s,"link",song.get('link'))
            ids.append(s.id)
        db.session.commit()
        payload = {
            "success":True,
            "ids":ids
        }
        songl = Song.query.get(song.get("id"))
        setattr(songl,"link",song.get("link"))
        db.session.commit()
    except Exception as error:
        payload = {
            "success":False,
            "errors":[str(error)]
        }
    return payload

@convert_kwargs_to_snake_case
def update_song_resolver(obj,info,song):
    try:
        assert(song.get('id'))
        songI = Songs.query.get(song.get('id'))
        assert(songI)
        if song.get('play_count'):
            #songI['play_count'] = song.get('play_count')
            setattr(songI,"play_count",song.get('play_count'));
        if song.get('title'):
            #songI['title'] = song.get('title')
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
    "createSong":create_song_resolver,
    "updateSong":update_song_resolver,
    "updateAllSongLinks":update_song_links
}

songs_resolver = {
    "queries":queries,
    "mutations":mutations
}