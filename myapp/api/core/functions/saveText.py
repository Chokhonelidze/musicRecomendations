from api.models import Song, Downlods, Songs, Song
from pytube import YouTube
import os
from api import db, translate
from pytube.innertube import _default_clients
from pytube import cipher
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

def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter."""
    function_patterns = [
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
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
    raise Exception("Could not find throttling function name")

def saveText(link, id):
    try:
        cipher.get_throttling_function_name = get_throttling_function_name
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
