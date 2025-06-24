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

