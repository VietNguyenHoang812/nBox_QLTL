from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.base import get_db
from app.repositories.file_repository import FileRepository
from app.services.file_service import FileService
from app.models.file_model import FileResponse, FileUpdate, FileSearchParams

router = APIRouter()


# Dependency for FileService
def get_file_service(db: Session = Depends(get_db)):
    repository = FileRepository(db)
    return FileService(repository)


@router.post("/files/", response_model=FileResponse)
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    file_service: FileService = Depends(get_file_service)
):
    """Upload a file with optional description"""
    try:
        return await file_service.save_file(file, description)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")


@router.get("/files/", response_model=List[FileResponse])
def get_files(
    skip: int = 0,
    limit: int = 100,
    file_service: FileService = Depends(get_file_service)
):
    """Get all files with pagination"""
    return file_service.get_all_files(skip, limit)


@router.get("/files/{file_id}", response_model=FileResponse)
def get_file(
    file_id: int,
    file_service: FileService = Depends(get_file_service)
):
    """Get a specific file by ID"""
    file = file_service.get_file(file_id)
    if file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return file


@router.put("/files/{file_id}", response_model=FileResponse)
def update_file(
    file_id: int,
    file_update: FileUpdate,
    file_service: FileService = Depends(get_file_service)
):
    """Update file metadata"""
    updated_file = file_service.update_file(file_id, file_update)
    if updated_file is None:
        raise HTTPException(status_code=404, detail="File not found")
    return updated_file


@router.delete("/files/{file_id}", response_model=bool)
def delete_file(
    file_id: int,
    file_service: FileService = Depends(get_file_service)
):
    """Delete a file"""
    success = file_service.delete_file(file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return success


@router.get("/files/search/", response_model=List[FileResponse])
def search_files(
    filename: Optional[str] = Query(None),
    content_type: Optional[str] = Query(None),
    min_size: Optional[int] = Query(None),
    max_size: Optional[int] = Query(None),
    description: Optional[str] = Query(None),
    skip: int = 0,
    limit: int = 100,
    file_service: FileService = Depends(get_file_service)
):
    """Search files by various parameters"""
    search_params = FileSearchParams(
        filename=filename,
        content_type=content_type,
        min_size=min_size,
        max_size=max_size,
        description=description
    )
    return file_service.search_files(search_params, skip, limit)
