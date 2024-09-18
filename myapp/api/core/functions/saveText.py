
from api.models import Song,Downlods,Songs,Song
from ariadne import convert_kwargs_to_snake_case
from pytube import YouTube
import os
from api import db,translate
from pytube.innertube import _default_clients
from pytube import cipher
import re
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter

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

def saveText(link,id):
    try:
        chroma_client = chromadb.HttpClient(host="chroma", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
        sample_collection = chroma_client.get_or_create_collection(name="music",metadata={"hnsw:space": "cosine"})
        cipher.get_throttling_function_name = get_throttling_function_name
        ty = YouTube(str(link))
        video = ty.streams.filter(only_audio=True).first()
        destination = "/downloads/"
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        transcript=translate.transcribe(new_file)
        ob = Downlods(
            id = id,
            file=new_file,
            text= transcript['text']
        )
        songs = Songs.query.filter_by(song_id=id).all()
        ids = []
        for s in songs:
            setattr(s,"link",new_file)
            db.session.add(s)
        song = Song.query.get(id)      
        if song:
            setattr(song,"localLink",new_file)
        db.session.add(song)
        db.session.add(ob)
        db.session.commit()
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="nomic-ai/nomic-embed-text-v1")
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                encoding_name='cl100k_base',
                chunk_size=1024,
                chunk_overlap=32
            )
        text=text_splitter.split_text(transcript['text'])
        embeddings = sentence_transformer_ef(text)
        # embeddings = encoding.encode(transcript['text'])
        metadatas = []
        ids = []
        for x in range(len(text)):
            metadatas.append({"file":new_file,"id":str(id)})
            ids.append(str(id)+"_"+str(x))
        if  embeddings is not None:
            sample_collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)
            print(sample_collection.get(),flush=True)


        # encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
        # len(encoding.encode(transcript))

        return new_file
    except Exception as error:
        print("error=",error,flush=True)