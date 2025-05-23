import os
import shutil

from typing import List, Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.repositories.doc_repository import DocRepository
from app.repositories.file_repository import FileRepository
from app.models.file_model import FileCreate
from app.models.doc_model import DocCreate
from app.models.request_model import UploadRequest, DocumentSearchRequest
from app.config import settings


class DocService:
    def __init__(self, doc_repository: DocRepository):
        self.doc_repository = doc_repository
        self.file_repository = FileRepository()

        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async def upload_files(self, requests: List[UploadRequest], files: List[UploadFile]):
        """
        Upload multiple files with their corresponding request metadata
        """
        idx_start_file = 0
        for request in requests:
            print(request)

            # Check if update or create
            if request.is_update == False:
                doc_create = DocCreate(**request.metadata)
                doc_id = self.doc_repository.create(doc_create)

                # Save files of the request
                request_files = files[idx_start_file:idx_start_file + len(request.files)]
                for file in request_files:
                    # Save file to disk
                    path_folder, _ = await self.save_file(file, doc_id)

                    # Create file record in database
                    file_format = file.filename.split(".")[-1]
                    file_name = file.filename.split(".")[0]

                    file_create = FileCreate(
                        doc_id=doc_id,
                        file_name=file_name,
                        file_format=file_format[1:],
                        path_folder=path_folder,
                        pathfile=file.filename,
                    )

                    self.file_repository.create(file_create, doc_create.updated_by)
            else:
                pass

    async def save_file(self, file: UploadFile, doc_id: int):
        # Create file path
        path_folder = os.path.join(settings.UPLOAD_DIR, str(doc_id))
        full_pathfile = os.path.join(path_folder, file.filename)
        os.makedirs(path_folder, exist_ok=True)

        # Save file to disk
        with open(full_pathfile, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return path_folder, full_pathfile
    
    def update_file(self, file_id: int, file_update):
        db_file = self.doc_repository.update(file_id, file_update)
        # if db_file:
        #     return DocInDB.model_validate(db_file)
        # return None
    
    def delete_file(self, file_id: int) -> bool:
        file = self.doc_repository.get_by_id(file_id)
        if file:
            # Delete from filesystem if exists
            if os.path.exists(file.file_path):
                os.remove(file.file_path)
            # Delete from database
            return self.doc_repository.delete(file_id)
        return False
    
    # def search_files(self, params: FileSearchParams, skip: int = 0, limit: int = 100) -> List[DocInDB]:
    #     db_files = self.file_repository.search(params, skip, limit)
    #     return [DocInDB.model_validate(file) for file in db_files]
    
    async def search_documents(self, search_request: DocumentSearchRequest):
        """
        Hàm thực hiện tìm kiếm tài liệu với các bộ lọc được cung cấp
        """        
        try:
            result = self.doc_repository.search(search_request)
            if not result:
                return []
                
            return result
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error querying database: {str(e)}")