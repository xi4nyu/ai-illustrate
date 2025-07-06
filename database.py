import os
from contextlib import contextmanager

import chromadb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import CHROMA_COLLECTION_NAME, CHROMA_DATA_PATH, DATABASE_URL
from services.query import QueryMixin

# --- SQLAlchemy (DuckDB) Setup ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_db():
    db = SessionLocal()
    QueryMixin.db = db
    try:
        yield db
    finally:
        QueryMixin.db = None
        db.close()

Base = declarative_base()



# --- ChromaDB Setup ---

# Ensure the ChromaDB data directory exists
os.makedirs(CHROMA_DATA_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)
embedding_function = chromadb.utils.embedding_functions.DefaultEmbeddingFunction()

# Get or create the collection
vector_collection = client.get_or_create_collection(
    name=CHROMA_COLLECTION_NAME,
    embedding_function=embedding_function,
)


def get_vector_collection():
    return vector_collection
