import logging
import pandas as pd
import uuid

from typing import Union, List, Dict, Optional

from app.database.base import get_db_connection
from app.models.file_model import FileCreate, FileInDB


logger = logging.getLogger(__name__)

class FileRepository:
    def __init__(self):
        pass

    def create(self, file_create: FileCreate, updated_by: str) -> int:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                # Generate a unique ID for the file
                id = f"{file_create.doc_id}_{str(uuid.uuid4())}"

                query = """
                    INSERT INTO files (
                        id, doc_id, file_name, file_format,
                        file_role, path_folder, pathfile,
                        created_at, updated_at, updated_by 
                    )
                    VALUES (
                        %s, %s, %s, %s, 
                        %s, %s, %s,
                        NOW(), NOW(), %s
                    )
                """
                values = (
                    id, file_create.doc_id, file_create.file_name, file_create.file_format,
                    file_create.file_role, file_create.path_folder, file_create.pathfile,
                    updated_by
                )

                cur.execute(query, values)
                conn.commit()

                return id

    def get(self, file_id: int):
        pass

    def search(self, doc_id: str) -> List[FileInDB]:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT * FROM files WHERE doc_id = %s
                """
                cur.execute(query, (doc_id,))
                columns = [desc[0] for desc in cur.description]
                rows = cur.fetchall()

                return [FileInDB(**dict(zip(columns, row))) for row in rows]

    def update(self, file_id: int, update_data) -> Optional[dict]:
        pass

    def delete(self, file_id: int) -> bool:
        pass