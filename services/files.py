import hashlib
import os

from models.file import File
from services.base import BaseService
from tasks import delete_file_vector_task


class FileService(BaseService):
    _model = File

    def get_file(self, file_id: int):
        return self.get_one(id=file_id)

    def get_files_by_user(self, user_id: int, skip: int = 0, limit: int = 100):
        page = skip // limit + 1
        return self.get_list(page=page, limit=limit, joined_user=False, user_id=user_id)

    def get_all_files(self, skip: int = 0, limit: int = 100):
        page = skip // limit + 1
        return self.get_list(page=page, limit=limit, joined_user=False)

    def create_file_record(self, file_data: dict):
        return self.insert(file_data)

    def delete_file(self, file_id: int):
        db_file = self.get_file(file_id)
        if db_file:
            # Also delete the actual file from the filesystem
            if os.path.exists(db_file.file_path):
                os.remove(db_file.file_path)

            # Trigger deletion from the vector DB
            delete_file_vector_task.delay(db_file.hash)

            self.db.delete(db_file)
            self.db.commit()
        return db_file

    @staticmethod
    def calculate_file_hash(file_path: str):
        """Calculates the MD5 hash of a file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
