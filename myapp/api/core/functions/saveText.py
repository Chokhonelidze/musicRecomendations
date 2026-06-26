from api.models import Song, Downlods, Songs, Song
from pytubefix import YouTube  # Changed from pytube to pytubefix
import os
from api import db, translate
from pytubefix.innertube import _default_clients  # Changed from pytube to pytubefix
from pytubefix import cipher  # Changed from pytube to pytubefix
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb.utils import embedding_functions
import json

_default_clients["ANDROID"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["ANDROID_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_EMBED"]["context"]["client"]["clientVersion"] = "19.08.35"
_default_clients["IOS_MUSIC"]["context"]["client"]["clientVersion"] = "6.41"
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


def saveText(link, id):
    try:
        
        ty = YouTube(str(link))
  
        video = ty.streams.filter(only_audio=True).first()
        destination = "/downloads/"
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        
        transcript = translate.transcribe(new_file)
        
        # Save to database
        ob = Downlods(
            id=id,
            file=new_file,
            text=transcript['text']
        )
        db.session.add(ob)
        
        songs = Songs.query.filter_by(song_id=id).all()
        for s in songs:
            setattr(s, "link", new_file)
            db.session.add(s)
        
        song = Song.query.get(id)
        if song:
            setattr(song, "localLink", new_file)
            db.session.add(song)
        
        db.session.commit()
        
        # Generate embeddings and store in PostgreSQL
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="nomic-ai/nomic-embed-text-v1"
        )
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            encoding_name='cl100k_base',
            chunk_size=1024,
            chunk_overlap=32
        )
        text_chunks = text_splitter.split_text(transcript['text'])
        embeddings = sentence_transformer_ef(text_chunks)
        
        # Store embeddings in PostgreSQL (using your existing DB model)
        for idx, (chunk, embedding) in enumerate(zip(text_chunks, embeddings)):
            # Create a model instance for embeddings (you'll need to add this model)
            embedding_record = EmbeddingRecord(
                song_id=id,
                chunk_index=idx,
                text=chunk,
                embedding=json.dumps(embedding),  # Store as JSON
                file_path=new_file
            )
            db.session.add(embedding_record)
        
        db.session.commit()
        return new_file
        
    except Exception as error:
        print("error=", error, flush=True)
        db.session.rollback()
