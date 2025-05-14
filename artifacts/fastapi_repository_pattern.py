# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.database.base import engine, Base
from app.routers import file_router
from app.config import settings

# NOTE: In production, you would typically use alembic for migrations
# instead of creating tables directly
Base.metadata.create_all(bind=engine)

app = FastAPI(title="File Storage API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(file_router.router, prefix="/api", tags=["files"])

@app.get("/")
def read_root():
    return {"message": "Welcome to File Storage API"}


# config.py
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # PostgreSQL connection settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "file_storage"
    
    # Directory to store uploaded files
    UPLOAD_DIR: str = "./uploads"
    
    @property
    def DATABASE_URL(self) -> str:
        """Construct the database URL from settings."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"


settings = Settings()


# database/base.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# Create SQLAlchemy engine for PostgreSQL
engine = create_engine(
    settings.DATABASE_URL
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# database/models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, BigInteger
from sqlalchemy.sql import func
from app.database.base import Base


class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), index=True)
    file_path = Column(String(500))
    content_type = Column(String(100))
    file_size = Column(BigInteger)  # Use BigInteger for larger file sizes
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<File {self.filename}>"


# models/file_model.py
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


# repositories/file_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.models import File
from app.models.file_model import FileCreate, FileUpdate, FileSearchParams


class FileRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, file_data: dict) -> File:
        db_file = File(**file_data)
        self.db.add(db_file)
        self.db.commit()
        self.db.refresh(db_file)
        return db_file
    
    def get_by_id(self, file_id: int) -> Optional[File]:
        return self.db.query(File).filter(File.id == file_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[File]:
        return self.db.query(File).offset(skip).limit(limit).all()
    
    def update(self, file_id: int, update_data: FileUpdate) -> Optional[File]:
        db_file = self.get_by_id(file_id)
        if db_file:
            update_dict = update_data.dict(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(db_file, key, value)
            self.db.commit()
            self.db.refresh(db_file)
        return db_file
    
    def delete(self, file_id: int) -> bool:
        db_file = self.get_by_id(file_id)
        if db_file:
            self.db.delete(db_file)
            self.db.commit()
            return True
        return False
    
    def search(self, params: FileSearchParams, skip: int = 0, limit: int = 100) -> List[File]:
        query = self.db.query(File)
        
        if params.filename:
            query = query.filter(File.filename.ilike(f"%{params.filename}%"))
        
        if params.content_type:
            query = query.filter(File.content_type == params.content_type)
        
        if params.min_size is not None:
            query = query.filter(File.file_size >= params.min_size)
        
        if params.max_size is not None:
            query = query.filter(File.file_size <= params.max_size)
        
        if params.description:
            query = query.filter(File.description.ilike(f"%{params.description}%"))
        
        return query.offset(skip).limit(limit).all()


# services/file_service.py
import os
import shutil
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.repositories.file_repository import FileRepository
from app.models.file_model import FileCreate, FileUpdate, FileSearchParams, FileInDB
from app.config import settings


class FileService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository
        # Ensure upload directory exists
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    async def save_file(self, file: UploadFile, description: Optional[str] = None) -> FileInDB:
        # Create file path
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Prepare data for DB
        file_data = {
            "filename": file.filename,
            "file_path": file_path,
            "content_type": file.content_type,
            "file_size": file_size,
            "description": description
        }
        
        # Save to database
        db_file = self.file_repository.create(file_data)
        return FileInDB.model_validate(db_file)
    
    def get_file(self, file_id: int) -> Optional[FileInDB]:
        db_file = self.file_repository.get_by_id(file_id)
        if db_file:
            return FileInDB.model_validate(db_file)
        return None
    
    def get_all_files(self, skip: int = 0, limit: int = 100) -> List[FileInDB]:
        db_files = self.file_repository.get_all(skip, limit)
        return [FileInDB.model_validate(file) for file in db_files]
    
    def update_file(self, file_id: int, file_update: FileUpdate) -> Optional[FileInDB]:
        db_file = self.file_repository.update(file_id, file_update)
        if db_file:
            return FileInDB.model_validate(db_file)
        return None
    
    def delete_file(self, file_id: int) -> bool:
        file = self.file_repository.get_by_id(file_id)
        if file:
            # Delete from filesystem if exists
            if os.path.exists(file.file_path):
                os.remove(file.file_path)
            # Delete from database
            return self.file_repository.delete(file_id)
        return False
    
    def search_files(self, params: FileSearchParams, skip: int = 0, limit: int = 100) -> List[FileInDB]:
        db_files = self.file_repository.search(params, skip, limit)
        return [FileInDB.model_validate(file) for file in db_files]


# routers/file_router.py
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
