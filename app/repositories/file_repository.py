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