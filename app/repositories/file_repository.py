import logging
import pandas as pd

from typing import Union, List, Dict, Optional
from app.database.base import get_db_connection
from app.models.file_model import FileUpdate
from app.models.request_model import DocumentSearchRequest


logger = logging.getLogger(__name__)

class FileRepository:
    def update(self, file_id: int, update_data: FileUpdate) -> Optional[dict]:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                update_dict = update_data.model_dump(exclude_unset=True)
                set_clause = ", ".join(f"{key} = %s" for key in update_dict.keys())
                values = list(update_dict.values()) + [file_id]
                cur.execute(
                    f"UPDATE files SET {set_clause} WHERE id = %s RETURNING *",
                    values
                )
                conn.commit()
                return cur.fetchone()

    def delete(self, file_id: int) -> bool:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM files WHERE id = %s",
                    (file_id,)
                )
                conn.commit()
                return cur.rowcount > 0

    def search(self, search_request: DocumentSearchRequest) -> Union[List[Dict], Dict[str, str]]:
        """
        Hàm thực hiện tìm kiếm tài liệu với các bộ lọc được cung cấp
        """
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    # Xây dựng câu query SQL động dựa trên các tham số được cung cấp
                    query = "SELECT * FROM fake_db WHERE 1=1"
                    doc_name = search_request.doc_name
                    option_doc = search_request.option_doc
                    field = search_request.field
                    doc_type = search_request.doc_type
                    params = []
                    
                    if doc_name:
                        query += " AND doc_name ILIKE %s"
                        params.append(f"%{doc_name}%")
                    
                    if option_doc:
                        query += " AND option_doc = %s"
                        params.append(option_doc)
                    
                    if field:
                        query += " AND field = %s"
                        params.append(field)
                        
                    if doc_type:
                        query += " AND doc_type = %s"
                        params.append(doc_type)
        
                    cur.execute(query, params)
                    columns = [desc[0] for desc in cur.description]
                    rows = cur.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
        
        except Exception as e:
            logger.error(f"Database error in search: {str(e)}")
            return {
                "status": "error",
                "message": "Database operation failed",
                "details": str(e)
            }