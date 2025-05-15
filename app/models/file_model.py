from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FileBase(BaseModel):
    description: Optional[str] = None


class FileCreate(FileBase):
    pass


class FileUpdate(FileBase):
    description: Optional[str] = None


class FileInDB(FileBase):
    id: str
    option_id: int
    doc_name: str
    doc_code: Optional[str] = None
    date_publish: Optional[str] = None
    date_expire: Optional[str] = None
    version: Optional[int] = None
    author: Optional[str] = None
    approver: Optional[str] = None
    year_publish: Optional[str] = None
    field: str
    doc_type: Optional[str] = None
    validity: str
    status: str
    updated_by: str
    leader_approver: str
    updated_at: Optional[datetime] = None


class FileResponse(FileInDB):
    pass


class FileSearchParams(BaseModel):
    filename: Optional[str] = None
    content_type: Optional[str] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    description: Optional[str] = None

class DocumentSearchRequest(BaseModel):
    doc_name: Optional[str] = None
    option_doc: Optional[int] = None
    field: Optional[str] = None
    doc_type: Optional[str] = None