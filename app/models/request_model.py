from pydantic import BaseModel
from typing import List, Optional


class UploadRequest(BaseModel):
    request_id: str
    name: str
    created_by: str
    leader_approver: str
    metadata: Optional[List[dict]]

class DocumentUploadRequest(BaseModel):
    option_doc: str
    option: bool
    id_update: Optional[str] = None
    doc_name: str
    doc_code: Optional[str] = None
    date_publish: Optional[str] = None
    date_expire: Optional[str] = None
    version: Optional[str] = None
    author: Optional[str] = None
    approver: Optional[str] = None
    field: str
    doc_type: Optional[str] = None
    file: List
    file_other: Optional[List] = None
    year_publish: Optional[str] = None

class DocumentSearchRequest(BaseModel):
    doc_name: Optional[str] = None
    option_doc: Optional[str] = None
    field: Optional[str] = None
    doc_type: Optional[str] = None