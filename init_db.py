from database import engine, Base
from sqlalchemy import text
from models import conversation, thread, user


def init_db():
    # Import all models here to ensure they are registered on the metadata

    # Create sequences for DuckDB
    with engine.connect() as conn:
        conn.execute(text("CREATE SEQUENCE IF NOT EXISTS users_id_seq"))
        conn.execute(text("CREATE SEQUENCE IF NOT EXISTS conversation_id_seq"))
        conn.execute(text("CREATE SEQUENCE IF NOT EXISTS thread_id_seq"))
        conn.execute(text("CREATE SEQUENCE IF NOT EXISTS files_id_seq"))
        conn.commit()

    Base.metadata.create_all(bind=engine)
