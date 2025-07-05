# Database Configuration
DATABASE_URL = "duckdb:///./ai_illustrate.db"

# ChromaDB Configuration
CHROMA_DATA_PATH = ".chromadb"
CHROMA_COLLECTION_NAME = "text_collection"

# Celery 配置
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
