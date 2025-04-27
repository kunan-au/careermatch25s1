import logging
import sys
import os.path
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
)
import nest_asyncio

import openai

from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
import chromadb

openai.api_key = os.getenv("OPENAI_API_KEY")

nest_asyncio.apply()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

PERSIST_DIR = "./storage"
CHROMA_COLLECTION_NAME = "my_collection"


def create_vector_storage():
    # Check if storage already exists
    if not os.path.exists(PERSIST_DIR):
        # Create Chroma client
        chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)
        
        # Create or get Chroma collection
        chroma_collection = chroma_client.get_or_create_collection(CHROMA_COLLECTION_NAME)
        
        # Create Chroma vector store
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        
        # Create storage context
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Load the documents
        documents = SimpleDirectoryReader("data/").load_data()
        
        # Create the index with Chroma vector store
        index = VectorStoreIndex.from_documents(
            documents, 
            storage_context=storage_context,
            embed_model=OpenAIEmbedding()
        )
        
        # Note: No need to explicitly persist as Chroma PersistentClient 
        # automatically saves to disk
        logging.info(f"Vector storage created and saved to {PERSIST_DIR}")
    else:
        logging.error(f"{PERSIST_DIR} already exists")


if __name__ == "__main__":
    create_vector_storage()
