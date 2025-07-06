import hashlib
import os

from models import File
from services.base import BaseService


class FileService(BaseService):
    _model = File

    @classmethod
    def get_file(cls, file_id: int):
        return cls.get_one(id=file_id)

    @classmethod
    def get_files_by_user(cls, user_id: int, page: int = 1, limit: int = 20):
        return cls.get_list(page=page, limit=limit, joined_user=False, user_id=user_id)

    @classmethod
    def get_all_files(cls, page: int = 1, limit: int = 20):
        return cls.get_list(page=page, limit=limit, joined_user=False)

    @classmethod
    def create_file_record(cls, file_data: dict):
        return cls.insert(file_data)

    @classmethod
    def delete_file(cls, file_id: int):
        db_file = cls.get_file(file_id)
        if db_file:
            # Also delete the actual file from the filesystem
            if os.path.exists(db_file.file_path):
                os.remove(db_file.file_path)

            # Trigger deletion from the vector DB
            # TODO:
            # delete_file_vector_task.delay(db_file.hash)

            cls.delete(db_file.id)
        return db_file

    @classmethod
    def calculate_file_hash(cls, file_path: str):
        """Calculates the MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
