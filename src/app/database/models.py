from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.base import Base


class File(Base):
    __tablename__ = "fake_db"
    
    id = Column(Integer, primary_key=True, index=True)
    option_doc = Column(Integer, nullable=False)
    doc_name = Column(String(255), nullable=False)
    doc_code = Column(String(255), nullable=True)
    date_publish = Column(DateTime(timezone=True), nullable=True)
    date_expire = Column(DateTime(timezone=True), nullable=True)
    version = Column(String(50), nullable=True)
    author = Column(String(100), nullable=True)
    approver = Column(String(100), nullable=True)
    year_publish = Column(String(4), nullable=True)
    field = Column(String(100), nullable=False)
    doc_type = Column(String(100), nullable=True)
    validity = Column(String(50), nullable=True)
    status = Column(String(50), nullable=True)
    updated_by = Column(String(100), nullable=False)
    leader_approver = Column(String(100), nullable=True)
    updated_time = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<File {self.filename}>"