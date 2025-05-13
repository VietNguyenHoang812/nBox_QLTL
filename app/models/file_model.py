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
    id: int
    filename: str
    file_path: str
    content_type: str
    file_size: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class FileResponse(FileInDB):
    pass


class FileSearchParams(BaseModel):
    filename: Optional[str] = None
    content_type: Optional[str] = None
    min_size: Optional[int] = None
    max_size: Optional[int] = None
    description: Optional[str] = None