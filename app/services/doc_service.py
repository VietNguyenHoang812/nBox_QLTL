import os
import shutil

from typing import List, Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from app.repositories.doc_repository import DocRepository
from app.repositories.file_repository import FileRepository
from app.models.file_model import FileCreate
from app.models.doc_model import DocCreate
from app.models.request_model import DocumentSearchRequest, DocumentUploadRequest
from app.models.response_model import DocumentSearchResponse
from app.config import settings


CREATE = 1
UPDATE = 2

class DocService:
    def __init__(self, doc_repository: DocRepository):
        self.doc_repository = doc_repository
        self.file_repository = FileRepository()

        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async def upload_documents(self, document_requests: List[DocumentUploadRequest], created_by: str="vietnh41", leader_approver: str="vietnh41"):
        """
        Upload multiple files with their corresponding request metadata
        """
        for request in document_requests:
            # Check if update or create
            if request.option == CREATE:
                await self.create_document(request, created_by, leader_approver)
            else:
                await self.update_document(request, created_by, leader_approver)

    async def save_file(self, file, doc_id: int):
        # Create file path
        filename = file
        path_folder = os.path.join(settings.UPLOAD_DIR, str(doc_id))
        full_pathfile = os.path.join(path_folder, filename)
        os.makedirs(path_folder, exist_ok=True)

        # Save file to disk
        # with open(full_pathfile, "wb") as buffer:
        #     shutil.copyfileobj(file.file, buffer)

        return path_folder, full_pathfile
    
    async def create_document(self, request: DocumentUploadRequest, created_by: str, leader_approver: str):
        doc_create = DocCreate(
            **request.model_dump(),
            updated_by=created_by,
            leader_approver=leader_approver,
        )
        doc_id = self.doc_repository.create(doc_create)

        # Save files of the request
        files_main = request.file
        files_other = request.file_other if request.file_other else []
        for file in files_main:
            # Save file to disk
            # path_folder, _ = await self.save_file(file, doc_id)

            # Create file record in database
            filename = file.name
            file_format = filename.split(".")[-1]
            file_name = filename.split(".")[0]
            path_folder = file.file_url

            file_create = FileCreate(
                doc_id=doc_id,
                file_name=file_name,
                file_format=file_format,
                file_role="VB",  # Main file
                path_folder=path_folder,
                pathfile=filename,
            )

            self.file_repository.create(file_create, doc_create.updated_by)
        
        for file_other in files_other:
            # Save file to disk
            # path_folder, _ = await self.save_file(file_other, doc_id)

            # Create file record in database
            filename = file_other.name
            file_format = filename.split(".")[-1]
            file_name = filename.split(".")[0]
            path_folder = file.file_url

            file_create = FileCreate(
                doc_id=doc_id,
                file_name=file_name,
                file_format=file_format,
                path_folder=path_folder,
                pathfile=filename,
            )

            self.file_repository.create(file_create, doc_create.updated_by)
    
    async def update_document(self, request: DocumentUploadRequest, created_by: str, leader_approver: str):
        doc_create = DocCreate(
            **request.model_dump(),
            updated_by=created_by,
            leader_approver=leader_approver
        )

        # Update document
        doc_name = request.id_update
        doc_id = self.doc_repository.update(doc_name, doc_create)
        doc_id = doc_id[0]

        # Update files
        files_main = request.file
        files_other = request.file_other if request.file_other else []
        for file in files_main:
        #     # Save file to disk
        #     path_folder, _ = await self.save_file(file, doc_id)

            # Delete old files record in database
            self.file_repository.delete_by_doc_id(doc_id)

            # Create file record in database
            filename = file.name
            file_format = filename.split(".")[-1]
            file_name = filename.split(".")[0]
            path_folder = file.file_url

            file_create = FileCreate(
                doc_id=doc_id,
                file_name=file_name,
                file_format=file_format,
                file_role="VB",  # Main file
                path_folder=path_folder,
                pathfile=filename,
            )

            self.file_repository.create(file_create, doc_create.updated_by)
        
        for file_other in files_other:
            # Save file to disk
            # path_folder, _ = await self.save_file(file_other, doc_id)

            # Create file record in database
            filename = file_other
            file_format = filename.split(".")[-1]
            file_name = filename.split(".")[0]
            path_folder = file.file_url

            file_other_create = FileCreate(
                doc_id=doc_id,
                file_name=file_name,
                file_format=file_format,
                path_folder=path_folder,
                pathfile=filename,
            )

            self.file_repository.create(file_other_create, doc_create.updated_by)

    def delete_file(self, file_id: int) -> bool:
        file = self.doc_repository.get_by_id(file_id)
        if file:
            # Delete from filesystem if exists
            if os.path.exists(file.file_path):
                os.remove(file.file_path)
            # Delete from database
            return self.doc_repository.delete(file_id)
        return False
    
    async def search_documents(self, search_request: DocumentSearchRequest) -> List[DocumentSearchResponse]:
        """
        Hàm thực hiện tìm kiếm tài liệu với các bộ lọc được cung cấp
        """        
        try:
            list_docs = self.doc_repository.search(search_request)
            list_reponse = []
            for doc in list_docs:
                doc_id = doc.id
                # Get files associated with the document
                list_files = self.file_repository.search(doc_id)
                main_files, other_files = [], []
                for file in list_files:
                    # Check if the file is a main file
                    if file.file_role == "VB":
                        main_files.append(file.pathfile)
                    else:
                        other_files.append(file.pathfile)
                
                doc_search_response = DocumentSearchResponse(
                    id=doc.id,
                    option_doc=doc.option_doc,
                    doc_name=doc.doc_name,
                    doc_code=doc.doc_code,
                    date_publish=doc.date_publish,
                    date_expire=doc.date_expire,
                    version=doc.version,
                    author=doc.author,
                    approver=doc.approver,
                    year_publish=doc.year_publish,
                    field=doc.field,
                    doc_type=doc.doc_type,
                    file=main_files,
                    file_other=other_files,
                    validity=doc.validity,
                    status=doc.status,
                    updated_by=doc.updated_by,
                    leader_approver=doc.leader_approver,
                    updated_at=doc.updated_at
                )
                list_reponse.append(doc_search_response)
                
            return list_reponse
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error searching documents: {str(e)}")