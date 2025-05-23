from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DocCreate(BaseModel):
    option_doc: int
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
    updated_by: str
    leader_approver: str


class DocInDB(BaseModel):
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


class DocSearchRequest(BaseModel):
    doc_name: Optional[str] = None
    option_doc: Optional[int] = None
    field: Optional[str] = None
    doc_type: Optional[str] = None