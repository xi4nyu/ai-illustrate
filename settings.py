# Database Configuration
DATABASE_URL = "duckdb:///./ai_illustrate.db"

# ChromaDB Configuration
CHROMA_DATA_PATH = ".chromadb"
CHROMA_COLLECTION_NAME = "text_collection"

# Celery 配置
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

# JWT Configuration
SECRET_KEY = "89df76d588e74e1b8e7b2d790537c549"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60 * 24 * 30

