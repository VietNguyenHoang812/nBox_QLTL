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
    doc_code: str
    date_publish: str
    date_expire: str
    version: str
    author: str
    approver: str
    year_publish: str
    field: str
    doc_type: str
    validity: str
    status: str
    updated_by: str
    leader_approver: str
    updated_time: Optional[datetime] = None


class FileResponse(FileInDB):
    pass


class FileSearchParams(BaseModel):
    filename: Optional[str] = None
    content_type: Optional[str] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    description: Optional[str] = None