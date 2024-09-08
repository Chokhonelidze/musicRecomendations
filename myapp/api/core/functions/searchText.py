import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

def getSongs(songText):
    try:
        chroma_client = chromadb.HttpClient(host="chroma", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
        sample_collection = chroma_client.get_or_create_collection(name="music")
        sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        embeddings = sentence_transformer_ef(songText)
        data = sample_collection.query(
            query_embeddings=embeddings[0],
            n_results=2
        )
        print("test=",data)
        return data["ids"][0]
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