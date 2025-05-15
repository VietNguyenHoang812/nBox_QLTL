from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class UploadRequest(BaseModel):
    request_id: str
    is_update: bool = False
    metadata: Optional[dict] = None
    files: List[str]

class DocumentSearchRequest(BaseModel):
    doc_name: Optional[str] = None
    option_doc: Optional[int] = None
    field: Optional[str] = None
    doc_type: Optional[str] = None