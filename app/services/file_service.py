import os
import shutil
from typing import List, Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.repositories.file_repository import FileRepository
# from app.models.file_model import Doc
from app.models.doc_model import DocCreate
from app.models.request_model import UploadRequest, DocumentSearchRequest
from app.config import settings


class FileService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async def upload_files(self, requests: List[UploadRequest], files: List[UploadFile]):
        """
        Upload multiple files with their corresponding request metadata
        """
        for request in requests:
            doc_create = DocCreate(**request.metadata)
            doc_id = self.file_repository.create_doc(doc_create)


        
            pass

    async def save_file(self, file: UploadFile):
        pass
        # Create file path
        # file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        
        # # Save file to disk
        # with open(file_path, "wb") as buffer:
        #     shutil.copyfileobj(file.file, buffer)
        
        # # Get file size
        # file_size = os.path.getsize(file_path)
        
        # # Prepare data for DB
        # file_data = {
        #     "filename": file.filename,
        #     "file_path": file_path,
        #     "content_type": file.content_type,
        #     "file_size": file_size,
        #     "description": description
        # }
        
        # # Save to database
        # db_file = self.file_repository.create(file_data)
        # return DocInDB.model_validate(db_file)
    
    def update_file(self, file_id: int, file_update):
        db_file = self.file_repository.update(file_id, file_update)
        # if db_file:
        #     return DocInDB.model_validate(db_file)
        # return None
    
    def delete_file(self, file_id: int) -> bool:
        file = self.file_repository.get_by_id(file_id)
        if file:
            # Delete from filesystem if exists
            if os.path.exists(file.file_path):
                os.remove(file.file_path)
            # Delete from database
            return self.file_repository.delete(file_id)
        return False
    
    # def search_files(self, params: FileSearchParams, skip: int = 0, limit: int = 100) -> List[DocInDB]:
    #     db_files = self.file_repository.search(params, skip, limit)
    #     return [DocInDB.model_validate(file) for file in db_files]
    
    async def search_documents(self, search_request: DocumentSearchRequest):
        """
        Hàm thực hiện tìm kiếm tài liệu với các bộ lọc được cung cấp
        """        
        try:
            result = self.file_repository.search(search_request)
            if not result:
                return []
                
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error querying database: {str(e)}")