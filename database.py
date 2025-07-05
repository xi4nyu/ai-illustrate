from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import chromadb
import os

# --- SQLAlchemy (DuckDB) Setup ---
DATABASE_URL = "duckdb:///./ai_illustrate.db"

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
    from models.base import Base
    from models import user, file, thread, conversation
    Base.metadata.create_all(bind=engine)


# --- ChromaDB Setup ---
CHROMA_DATA_PATH = "chroma_data/"
CHROMA_COLLECTION_NAME = "text_collection"

# Ensure the ChromaDB data directory exists
os.makedirs(CHROMA_DATA_PATH, exist_ok=True)

client = chromadb.PersistentClient(path=CHROMA_DATA_PATH)

# Get or create the collection
try:
    vector_collection = client.get_collection(name=CHROMA_COLLECTION_NAME)
except Exception:
    vector_collection = client.create_collection(name=CHROMA_COLLECTION_NAME)

def get_vector_collection():
    return vector_collection
