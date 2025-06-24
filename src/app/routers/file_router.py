import json

from fastapi import APIRouter, Depends, HTTPException, Body, Request
from typing import List, Optional

from app.repositories.doc_repository import DocRepository
from app.services.doc_service import DocService
from app.models.file_model import FileUpload
from app.models.request_model import UploadRequest, DocumentSearchRequest, DocumentUploadRequest

router = APIRouter()


def get_file_service():
    repository = DocRepository()
    return DocService(repository)

@router.post("/batch-upload/")
async def batch_upload(
    request: Request,
):
    """
    Upload multiple files with their corresponding request metadata
    
    Args:
        requests: List of UploadRequest containing metadata for each batch
    """
    try:
        body = await request.body()
        if not body:
            raise HTTPException(status_code=400, detail="No data provided")
        # body = """{"request_id":"batch1","is_update":false,"description":"First batch of files","metadata":{"list_require":[{"option_doc":"1","option":"1","doc_name":"vietnh41_test_2306","doc_code":"AAA1234","date_publish":"2025-06-22","date_expire":"2025-06-24","version":1,"field":[{"value":"7","content":"H\\u1ea1 t\\u1ea7ng CNTT"}],"doc_type":"3","file":"[{\\"originalName\\":\\"1750642866_Ke_hoach_hop_tac_VTN-VAI_trong_phat_trien_ung_dung_AI_nam_2025.pdf\\",\\"host\\":\\"\\",\\"relLocation\\":\\"aws2\\/netmind\\/category_file_upload\\/1750642866_Ke_hoach_hop_tac_VTN-VAI_trong_phat_trien_ung_dung_AI_nam_2025.pdf\\",\\"file_url\\":\\"aws2\\/netmind\\/category_file_upload\\/1750642866_Ke_hoach_hop_tac_VTN-VAI_trong_phat_trien_ung_dung_AI_nam_2025.pdf\\",\\"id\\":6883275,\\"name\\":\\"Ke hoach hop tac VTN-VAI trong phat trien ung dung AI nam 2025.pdf\\",\\"thumbnail\\":\\"aws2\\/netmind\\/category_file_upload\\/1750642866_Ke_hoach_hop_tac_VTN-VAI_trong_phat_trien_ung_dung_AI_nam_2025.pdf\\",\\"fileType\\":\\"application\\/pdf\\",\\"size\\":507464,\\"shortLink\\":\\"ogPJSa\\",\\"signed\\":\\"\\"}]","file_other":"[{\\"originalName\\":\\"1750643497_ragflow_evaluation.xlsx\\",\\"host\\":\\"\\",\\"relLocation\\":\\"aws2\\/netmind\\/category_file_upload\\/1750643497_ragflow_evaluation.xlsx\\",\\"file_url\\":\\"aws2\\/netmind\\/category_file_upload\\/1750643497_ragflow_evaluation.xlsx\\",\\"id\\":6883279,\\"name\\":\\"ragflow_evaluation.xlsx\\",\\"thumbnail\\":\\"aws2\\/netmind\\/category_file_upload\\/1750643497_ragflow_evaluation.xlsx\\",\\"fileType\\":\\"application\\/vnd.openxmlformats-officedocument.spreadsheetml.sheet\\",\\"size\\":156733,\\"shortLink\\":\\"brwbOQ\\",\\"signed\\":\\"\\"}]","approver":13361,"author":"vietnh41"},{"option_doc":"4","option":"2","id_update":"T\\u00e0i li\\u1ec7u vendor Nokia","doc_name":"vendor2","field":[{"value":"1","content":"V\\u00f4 tuy\\u1ebfn"}],"doc_type":"t\\u00e0i li\\u1ec7u vendor","file":"[{\\"originalName\\":\\"1750643599_VBQL_left.xlsx\\",\\"host\\":\\"\\",\\"relLocation\\":\\"aws2\\/netmind\\/category_file_upload\\/1750643599_VBQL_left.xlsx\\",\\"file_url\\":\\"aws2\\/netmind\\/category_file_upload\\/1750643599_VBQL_left.xlsx\\",\\"id\\":6883281,\\"name\\":\\"VBQL_left.xlsx\\",\\"thumbnail\\":\\"aws2\\/netmind\\/category_file_upload\\/1750643599_VBQL_left.xlsx\\",\\"fileType\\":\\"application\\/vnd.openxmlformats-officedocument.spreadsheetml.sheet\\",\\"size\\":10431,\\"shortLink\\":\\"hqrfuc\\",\\"signed\\":\\"\\"}]"}]}}
        # """
        data = json.loads(body)
        if not isinstance(data, dict):
            raise HTTPException(status_code=400, detail="Invalid data format")
        
        list_require = data.get("metadata", {}).get("list_require", [])
        
        for item in list_require:
            item["version"] = str(item.get("version", 1))  # Ensure version is a string
            item["file"] = json.loads(item["file"]) if item.get("file") else []
            item["file_other"] = json.loads(item["file_other"]) if item.get("file_other") else []
            item["approver"] = str(item.get("approver", ""))  # Ensure approver is a string
            item["file"] = [FileUpload(**file) for file in item["file"]]
            item["file_other"] = [FileUpload(**file) for file in item["file_other"]]

        document_requests = [DocumentUploadRequest(**item) for item in list_require]

        # request = UploadRequest(**request)
        # metadatas, created_by, leader_approver = request.metadata, request.created_by, request.leader_approver
        # document_requests = [DocumentUploadRequest(**metadata) for metadata in metadatas]

        file_service = DocService(DocRepository())
        results  = await file_service.upload_documents(document_requests)

        return {
            "status": "success",
        }

    except Exception as e:
        print("Error in batch upload:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

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
