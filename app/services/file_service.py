import os
import shutil
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories.file_repository import FileRepository
from app.models.file_model import FileCreate, FileUpdate, FileSearchParams, FileInDB
from app.config import settings


class FileService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async def save_file(self, file: UploadFile, description: Optional[str] = None) -> FileInDB:
        # Create file path
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Prepare data for DB
        file_data = {
            "filename": file.filename,
            "file_path": file_path,
            "content_type": file.content_type,
            "file_size": file_size,
            "description": description
        }
        
        # Save to database
        db_file = self.file_repository.create(file_data)
        return FileInDB.model_validate(db_file)
    
    def get_file(self, file_id: int) -> Optional[FileInDB]:
        db_file = self.file_repository.get_by_id(file_id)
        if db_file:
            return db_file
        return None
    
    def get_all_files(self, skip: int = 0, limit: int = 100) -> List[FileInDB]:
        db_files = self.file_repository.get_all(skip, limit)
        return db_files
        # return [FileInDB.model_validate(file) for file in db_files]
    
    def update_file(self, file_id: int, file_update: FileUpdate) -> Optional[FileInDB]:
        db_file = self.file_repository.update(file_id, file_update)
        if db_file:
            return FileInDB.model_validate(db_file)
        return None
    
    def delete_file(self, file_id: int) -> bool:
        file = self.file_repository.get_by_id(file_id)
        if file:
            # Delete from filesystem if exists
            if os.path.exists(file.file_path):
                os.remove(file.file_path)
            # Delete from database
            return self.file_repository.delete(file_id)
        return False
    
    def search_files(self, params: FileSearchParams, skip: int = 0, limit: int = 100) -> List[FileInDB]:
        db_files = self.file_repository.search(params, skip, limit)
        return [FileInDB.model_validate(file) for file in db_files]