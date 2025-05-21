import logging
import pandas as pd

from typing import Union, List, Dict, Optional

from app.database.base import get_db_connection
from app.models.file_model import FileCreate, FileInDB


logger = logging.getLogger(__name__)

class FileRepository:
    def __init__(self):
        pass

    def create(self, file_create: FileCreate):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                id = ...  # Generate ID logic here
                validity = "Mới nhất"
                status = "Đã tiếp nhận"

                query = """
                    INSERT INTO files (
                        id, doc_id, file_name, file_format,
                        file_role, path_folder, pathfile,
                        created_at, updated_at, updated_by 
                    )
                    VALUES (
                        %s, %s, %s, %s, 
                        %s, %s, %s,
                        %s, %s, %s
                    )
                """
                values = (
                    id, file_create.doc_id, file_create.file_name, file_create.file_format,
                    file_create.file_role, file_create.path_folder, file_create.pathfile,
                    file_create.created_at, file_create.updated_at, file_create.updated_by
                )

                cur.execute(query, values)
                conn.commit()

                return id

    def get(self, file_id: int):
        pass

    def update(self, file_id: int, update_data) -> Optional[dict]:
        pass

    def delete(self, file_id: int) -> bool:
        pass