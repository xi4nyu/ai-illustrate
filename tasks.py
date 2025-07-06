import os

from sqlalchemy.orm import Session

from celery_app import app
from database import SessionLocal
from services import files
from utils import file_processor, vector_utils


@app.task
def process_file_task(file_id: int):
    """
    Celery task to process an uploaded file.
    1. Extracts text from the file.
    2. Adds the extracted text to the vector database.
    """
    db: Session = SessionLocal()
    try:
        db_file = files.get_file(db, file_id)
        if not db_file:
            print(f"File with id {file_id} not found.")
            return

        file_path = db_file.file_path
        file_name = db_file.name
        file_hash = db_file.hash

        # Determine file type from extension
        file_extension = os.path.splitext(file_name)[1].lower().replace(".", "")

        # 1. Extract text
        print(f"Processing file: {file_path}")
        extracted_text = file_processor.process_file(file_path, file_extension)

        if not extracted_text:
            print(f"No text could be extracted from {file_name}.")
            return

        # 2. Add to vector DB
        print(f"Adding text from {file_name} to vector database.")
        vector_utils.add_text_to_vector_db(
            file_hash=file_hash,
            file_name=file_name,
            file_type=file_extension,
            content=extracted_text,
        )
        print(f"Successfully processed and vectorized {file_name}.")

    finally:
        db.close()


@app.task
def delete_file_vector_task(file_hash: str):
    """
    Celery task to delete a file's vector from ChromaDB.
    """
    print(f"Deleting vector for file hash: {file_hash}")
    vector_utils.delete_vector(file_hash)
    print(f"Successfully deleted vector for file hash: {file_hash}")
