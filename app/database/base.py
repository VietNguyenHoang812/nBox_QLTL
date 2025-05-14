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

import psycopg2
from psycopg2.extras import RealDictCursor
from app.config import settings

def get_db_connection():
    return psycopg2.connect(
        host=settings.POSTGRES_HOST,
        database=settings.POSTGRES_DB,
        port=settings.POSTGRES_PORT,
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
    )