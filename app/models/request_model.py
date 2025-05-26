from pydantic import BaseModel
from typing import List, Optional


class UploadRequest(BaseModel):
    request_id: str
    name: str
    created_by: str
    metadata: Optional[List[dict]]

class DocumentSearchRequest(BaseModel):
    doc_name: Optional[str] = None
    option_doc: Optional[str] = None
    field: Optional[str] = None
    doc_type: Optional[str] = None