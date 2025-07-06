import hashlib
import os

from sqlalchemy.orm import Session

from models.file import File
from schemas.files import FileCreate
from tasks import delete_file_vector_task


def get_file(db: Session, file_id: int):
    return db.query(File).filter(File.id == file_id).first()


def get_files_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(File).filter(File.user_id == user_id).offset(skip).limit(limit).all()
    )


def get_all_files(db: Session, skip: int = 0, limit: int = 100):
    return db.query(File).offset(skip).limit(limit).all()


def create_file_record(db: Session, file_data: dict):
    db_file = File(**file_data)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file


def delete_file(db: Session, file_id: int):
    db_file = get_file(db, file_id)
    if db_file:
        # Also delete the actual file from the filesystem
        if os.path.exists(db_file.file_path):
            os.remove(db_file.file_path)

        # Trigger deletion from the vector DB
        delete_file_vector_task.delay(db_file.hash)

        db.delete(db_file)
        db.commit()
    return db_file


def calculate_file_hash(file_path: str):
    """Calculates the MD5 hash of a file."""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
