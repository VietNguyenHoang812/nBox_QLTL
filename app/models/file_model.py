from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class FileUpdate(BaseModel):
    description: Optional[str] = None

class FileCreate(BaseModel):
    doc_id: str
    file_name: str
    file_format: str
    file_role: Optional[str] = None
    path_folder: str
    pathfile: str

class FileInDB(BaseModel):
    id: str
    doc_id: str
    file_name: str
    file_format: str
    file_role: Optional[str] = None
    created_at: Optional[datetime] = None    
    updated_at: Optional[datetime] = None
    updated_by: str
    path_folder: str
    pathfile: str