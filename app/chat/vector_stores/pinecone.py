import os 
import pinecone
from langchain.vectorstores import Pinecone
from app.chat.embeddings.openai import embeddings 


# initialize our pinecone client 
pinecone.init(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENV_NAME")
)


# create vectorstores -> langchain wrapper 
vector_store = Pinecone.from_existing_index(
    os.getenv("PINECONE_INDEX_NAME"), embeddings
)

# can turn vector_store into retriever using;
# vector_store.as_retriever()