from pydantic import BaseModel
from typing import Dict, List, Optional

from app.models.file_model import FileUpload


class UploadRequest(BaseModel):
    request_id: str
    is_update: Optional[bool]
    description: Optional[str]
    metadata: Dict[str, List[dict]]

class DocumentUploadRequest(BaseModel):
    option_doc: str
    option: int
    id_update: Optional[str] = None
    doc_name: str
    doc_code: Optional[str] = None
    date_publish: Optional[str] = None
    date_expire: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    approver: Optional[str] = None
    field: List[Dict[str, str]]
    doc_type: Optional[str] = None
    file: List[FileUpload]
    file_other: Optional[List[FileUpload]] = None
    year_publish: Optional[str] = None

class DocumentSearchRequest(BaseModel):
    doc_name: Optional[str] = None
    option_doc: Optional[str] = None
    field: Optional[str] = None
    doc_type: Optional[str] = None