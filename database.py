import os

import chromadb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import CHROMA_COLLECTION_NAME, CHROMA_DATA_PATH, DATABASE_URL

# --- SQLAlchemy (DuckDB) Setup ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Import all models here to ensure they are registered on the metadata
    from models import conversation, file, thread, user
    from models.base import Base

    Base.metadata.create_all(bind=engine)


# --- ChromaDB Setup ---

# Ensure the ChromaDB data directory exists
os.makedirs(CHROMA_DATA_PATH, exist_ok=True)

client = chromadb.Client()

# Get or create the collection
vector_collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)


def get_vector_collection():
    return vector_collection
