import os
import shutil
from typing import List

from fastapi import APIRouter, HTTPException, UploadFile
from fastapi import File as FastAPIFile

from schemas.files import File
from services.files import FileService
from tasks import process_file_task
from settings import UPLOAD_DIRECTORY

router = APIRouter()


os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.post("/upload/", response_model=File)
async def upload_file(
    user_id: int, file: UploadFile = FastAPIFile(...)
):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    # Save the uploaded file
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # Calculate file hash
    file_hash = FileService.calculate_file_hash(file_location)

    # Create file record in the database
    file_create = {
        "user_id": user_id,
        "name": file.filename,
        "hash": file_hash,
        "file_path": file_location,
    }
    db_file = FileService.create_file_record(file_data=file_create)

    # Trigger the async task for file processing
    process_file_task.delay(db_file.id)

    return db_file


@router.get("/", response_model=List[File])
def list_files(skip: int = 0, limit: int = 100):
    files = FileService.get_all_files(skip=skip, limit=limit)
    return files


@router.get("/{file_id}", response_model=File)
def read_file(file_id: int):
    db_file = FileService.get_file(file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file


@router.delete("/{file_id}", response_model=File)
def delete_file(file_id: int):
    db_file = FileService.delete_file(file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return db_file
