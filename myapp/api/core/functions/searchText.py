import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from api.models import Downlods
from langchain.text_splitter import RecursiveCharacterTextSplitter


def restChroma(collection):
    try:
        chroma_client = chromadb.HttpClient(host="chroma", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
        chroma_client.delete_collection(collection)
    except Exception as error :
        print("error=",error,flush=True)


def loadDataToChroma(model_name="all-MiniLM-L6-v2",chunk_size=512,chunk_overlap=16):
    try:
        chroma_client = chromadb.HttpClient(host="chroma", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
        sample_collection = chroma_client.get_or_create_collection(name="music",metadata={"hnsw:space": "cosine"})
        data = Downlods.query.all()

        for d in data:
            #all-MiniLM-L6-v2
            sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model_name,trust_remote_code=True)
            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                encoding_name='cl100k_base',
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap
            )
            text=text_splitter.split_text(d.text)
            embeddings = sentence_transformer_ef(text)
            # embeddings = encoding.encode(transcript['text'])
            metadatas = []
            ids = []
            for x in range(len(text)):
                metadatas.append({"file":d.file,"id":str(d.id)})
                ids.append(str(d.id)+"_"+str(x))
            print(len(embeddings[0]))
            if embeddings is not None:
                sample_collection.add(embeddings=embeddings, metadatas=metadatas, ids=ids)
        print(len(sample_collection.get(include=['embeddings', 'metadatas'])['metadatas']),flush=True)
        

    except Exception as error:
        print("error=",error)


def getSongs(songText,model="all-MiniLM-L6-v2"):
    try:
        chroma_client = chromadb.HttpClient(host="chroma", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
        sample_collection = chroma_client.get_or_create_collection(name="music",metadata={"hnsw:space": "cosine"})
        #chroma_client.delete_collection("music")

     

        
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=model,trust_remote_code=True)
        embeddings = sentence_transformer_ef(songText)
        data = sample_collection.query(
            query_embeddings=embeddings,
            n_results=1,
            #where={"metadata_field": "is_equal_to_this"},
            # where_document={"$contains":"search_string"},
            include=["embeddings","metadatas","distances"]
        )
        print("test=",data)
        id_list =[]
        for d in data["metadatas"][0]:
            if 'id' in d.keys():
                id_list.append(d['id'])
        return id_list
        return []
    except Exception as error:
        print("error=",error,flush=True)


def deleteSongs(ids:list):
    try:
        chroma_client = chromadb.HttpClient(host="chroma", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
        sample_collection = chroma_client.get_or_create_collection(name="music")
        true = sample_collection.delete(ids=ids)
        print(true,flush=true)
    except Exception as error:
        print("error=",error,flush=True)