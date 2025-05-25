import json

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, Body
from typing import List, Optional

from app.repositories.doc_repository import DocRepository
from app.services.doc_service import DocService
from app.models.request_model import UploadRequest, DocumentSearchRequest

router = APIRouter()


def get_file_service():
    repository = DocRepository()
    return DocService(repository)

@router.post("/batch-upload/")
async def batch_upload(
    # requests_json: List[UploadRequest] = Form(...),
    requests_json: str = Form(...),
    files: List[UploadFile] = File(...),
):
    """
    Upload multiple files with their corresponding request metadata
    
    Args:
        requests: List of UploadRequest containing metadata for each batch
        files: List of files to upload
    """
    # try:
    # Parse the JSON string into a list of UploadRequest objects
    requests = json.loads(requests_json)["requests"]
    requests = [UploadRequest(**request) for request in requests]

    # Validate that number of files matches the total expected files
    total_expected_files = sum(len(req.files) for req in requests)
    if len(files) != total_expected_files:
        raise HTTPException(
            status_code=400,
            detail="Number of files doesn't match the request specifications"
        )

    file_service = DocService(DocRepository())
    results  = await file_service.upload_files(requests, files)

    return {
        "status": "success",
    }

    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

@router.post("/documents/search", tags=["Documents"])
async def search_documents_post(
    search_request: DocumentSearchRequest = Body(..., description="Thông tin tìm kiếm tài liệu")
):
    """
    Tìm kiếm tài liệu với các bộ lọc khác nhau qua Request Body.
    - Có thể tìm kiếm theo một hoặc nhiều tham số
    - Nếu không có tham số nào được truyền vào, trả về tất cả tài liệu
    """
    doc_service = DocService(DocRepository())
    docs = await doc_service.search_documents(search_request)

    return docs

@router.delete("/files/{file_id}", response_model=bool)
def delete_file(
    file_id: int,
    file_service: DocService = Depends(get_file_service)
):
    """Delete a file"""
    success = file_service.delete_file(file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return success
