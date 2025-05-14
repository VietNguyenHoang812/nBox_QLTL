import pandas as pd

from typing import List, Optional
from app.database.base import get_db_connection
from app.models.file_model import FileUpdate, FileSearchParams


class FileRepository:
    def get_by_id(self, file_id: int):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM fake_db WHERE id = 1"
                )
                rows = cur.fetchone()
                print(rows)
                colnames = [desc[0] for desc in cur.description]
                data = dict(zip(colnames, rows))
        print(data)
        return data

    def get_all(self, skip: int = 0, limit: int = 10):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM fake_db LIMIT %s OFFSET %s",
                    (limit, skip)
                )
                colnames = [desc[0] for desc in cur.description]
                rows = cur.fetchall()
                df = pd.DataFrame(rows, columns=colnames)
                print(df.to_dict(orient="records"))
            #     cur.close()
            # conn.close()
        
        return df.to_dict(orient="records")


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

    def search(self, params: FileSearchParams, skip: int = 0, limit: int = 100):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT * FROM files 
                    WHERE (%(filename)s IS NULL OR filename ILIKE %(filename_pattern)s)
                    AND (%(content_type)s IS NULL OR content_type = %(content_type)s)
                    LIMIT %(limit)s OFFSET %(skip)s
                """
                cur.execute(query, {
                    "filename": params.filename,
                    "filename_pattern": f"%{params.filename}%" if params.filename else None,
                    "content_type": params.content_type,
                    "limit": limit,
                    "skip": skip
                })
                return cur.fetchall()