import os
import shutil

from fastapi import APIRouter, HTTPException, UploadFile, Depends
from fastapi import File as FastAPIFile

from services.files import FileService
from tasks import process_file_task
from schemas.user import User
from schemas.api import R
from utils.jwt import get_current_user
from settings import UPLOAD_DIRECTORY

router = APIRouter()


os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


@router.post("/upload/")
async def upload_file(
    file: UploadFile = FastAPIFile(...),
    current_user: User = Depends(get_current_user),
):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    # Save the uploaded file
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    # Calculate file hash
    file_hash = FileService.calculate_file_hash(file_location)

    # Create file record in the database
    file_create = {
        "user_id": current_user.id,
        "name": file.filename,
        "hash": file_hash,
        "file_path": file_location,
        "updated_uid": current_user.id,
    }
    db_file = FileService.create_file_record(file_data=file_create)

    # Trigger the async task for file processing
    process_file_task.delay(db_file.id)

    return R(data=db_file)


@router.get("/")
def list_files(page: int = 1, limit: int = 20):
    files = FileService.get_all_files(page=page, limit=limit)
    return R(data=files)


@router.get("/{file_id}")
def read_file(file_id: int):
    db_file = FileService.get_file(file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return R(data=db_file)


@router.delete("/{file_id}")
def delete_file(file_id: int):
    db_file = FileService.delete_file(file_id=file_id)
    if db_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return R(data=db_file)
