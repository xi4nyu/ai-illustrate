import os

import chromadb
from sqlalchemy import create_engine, text
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

    # Create sequences for DuckDB
    with engine.connect() as conn:
        conn.execute(text("CREATE SEQUENCE IF NOT EXISTS users_id_seq"))
        conn.execute(text("CREATE SEQUENCE IF NOT EXISTS conversation_id_seq"))
        conn.execute(text("CREATE SEQUENCE IF NOT EXISTS thread_id_seq"))
        conn.execute(text("CREATE SEQUENCE IF NOT EXISTS files_id_seq"))
        conn.commit()

    Base.metadata.create_all(bind=engine)


# --- ChromaDB Setup ---

# Ensure the ChromaDB data directory exists
os.makedirs(CHROMA_DATA_PATH, exist_ok=True)

client = chromadb.Client()

# Get or create the collection
vector_collection = client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)


def get_vector_collection():
    return vector_collection
