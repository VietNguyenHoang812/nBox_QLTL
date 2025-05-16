from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class FileUpdate(BaseModel):
    description: Optional[str] = None


class FileInDB(BaseModel):
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
    updated_at: datetime = None


class FileResponse(BaseModel):
    pass