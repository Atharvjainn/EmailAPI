import os
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

pc = Pinecone(api_key=os.getenv('PINECONE_API_KEY'))

index_name = os.getenv('PINECONE_INDEX_NAME')
index = pc.Index(index_name)

embeddings_model = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

def get_vector_store(namespace : str):
    return PineconeVectorStore(
        index_name=index_name,
        embedding=embeddings_model,
        namespace=namespace
    )


def get_retriever(namespace : str,k : int = 10):
    return get_vector_store(namespace=namespace).as_retriever(search_type='similarity', search_kwargs={"k": k})

