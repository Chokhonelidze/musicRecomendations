from ariadne import convert_kwargs_to_snake_case
from api import db
from ..models import Songs
from surprise.reader import Reader
from sqlalchemy import text
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
        gs_optimized = KNNBasic(sim_options={'name':'pearson_baseline','user_based': True}, k=30, min_k=9, verbose=False)
        df = pd.read_sql_table('Songs',con=db.get_engine(),index_col='id')
        print(df.head())
        #df = pd.read_csv('final_data.csv')
        reader = Reader(rating_scale=(0,5))
        data = Dataset.load_from_df(df[['user_id', 'song_id', 'play_count']], reader) 
        trainset = data.build_full_trainset()
        gs_optimized.fit(trainset)
        #p_play_count_play = gs_optimized.predict(query['user_id'],query["song_id"],verbose=True)
        #print(p_play_count_play)
        df_rating=df.drop_duplicates()
        recommendations =get_recommendations(df_rating,query.get("user_id"),5,gs_optimized)
        print(recommendations)
        payload = {
            "success":True,
            "predict":recommendations
        }
    except Exception as error:
        payload = {
            "success":False,
            "errors":[str(error)]
        }
    return payload

    
@convert_kwargs_to_snake_case
def list_songs_resolver(obj,info,filters=None):
    try:
        if filters.get('user'):
            songs = [song.to_dict() for song in Songs.query.filter_by(user_id =filters['user']).all()];
        elif filters.get("search"):
            if filters['filter'] == 'title':
                songs =  [song.to_dict() for song in Songs.query.filter((Songs.title.like("%"+filters['search']+"%")) & (Songs.user_id != filters['user'])).group_by('song_id').all()]
            elif filters['filter'] == 'release':
                songs =  [song.to_dict() for song in Songs.query.filter((Songs.release.like("%"+filters['search']+"%")) & (Songs.user_id != filters['user'])).group_by('song_id').all()]
            elif filters['filter'] == 'artist_name':
                songs =  [song.to_dict() for song in Songs.query.filter((Songs.artist_name.like("%"+filters['search']+"%")) & (Songs.user_id != filters['user'])).group_by('song_id').all()]
            elif filters['filter'] == 'year':
                songs =  [song.to_dict() for song in Songs.query.filter((Songs.year.like("%"+filters['search']+"%")) & (Songs.user_id != filters['user'])).group_by('song_id').all()]

        else:
             songs =  [song.to_dict() for song in Songs.query.group_by('song_id').all()] 
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
        print(Songs.query.filter_by(song_id=id).first())
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
        songI = Songs(
            user_id = song['user_id'],
            song_id = song['song_id'],
            play_count = song['play_count'],
            title = song['title'],
            release = song['release'],
            artist_name = song['artist_name'],
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
def update_song_resolver(obj,info,song):
    try:
        assert(song.get('id'))
        songI = Songs.query.get(song.get('id'))
        assert(songI)
        if song.get('play_count'):
            songI['play_count'] = song.get('play_count')
        if song.get('title'):
            songI['title'] = song.get('title')
        if(song.get('release')):
            songI['release'] = song.get('release')
        if(song.get('artist_name')):
            songI['artist_name'] = song.get('artist_name')
        if(song.get('year')):
            songI['year'] = song.get('year')
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
    "updateSong":update_song_resolver
}

songs_resolver = {
    "queries":queries,
    "mutations":mutations
}