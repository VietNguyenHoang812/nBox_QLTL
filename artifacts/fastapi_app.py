from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from datetime import datetime

# Khởi tạo ứng dụng FastAPI
app = FastAPI(
    title="API Demo",
    description="Ứng dụng FastAPI mẫu",
    version="1.0.0"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường thực tế, bạn nên giới hạn origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model dữ liệu
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    created_at: Optional[datetime] = None

# Giả lập database đơn giản
items_db = []
item_id_counter = 1

# Routes
@app.get("/")
async def root():
    """Endpoint chào mừng"""
    return {"message": "Chào mừng đến với API của tôi"}

@app.get("/items", response_model=List[Item])
async def get_items():
    """Lấy danh sách tất cả các items"""
    return items_db

@app.get("/items/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Lấy thông tin một item theo ID"""
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item không tồn tại")

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    """Tạo một item mới"""
    global item_id_counter
    
    # Thêm ID và thời gian tạo
    item.id = item_id_counter
    item.created_at = datetime.now()
    
    # Tăng biến đếm ID
    item_id_counter += 1
    
    # Thêm vào database
    items_db.append(item)
    return item

@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: int, updated_item: Item):
    """Cập nhật thông tin một item"""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            # Giữ nguyên ID và thời gian tạo
            updated_item.id = item_id
            updated_item.created_at = item.created_at
            
            # Cập nhật item trong database
            items_db[i] = updated_item
            return updated_item
    
    raise HTTPException(status_code=404, detail="Item không tồn tại")

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    """Xóa một item"""
    for i, item in enumerate(items_db):
        if item.id == item_id:
            # Xóa item khỏi database
            items_db.pop(i)
            return
    
    raise HTTPException(status_code=404, detail="Item không tồn tại")

# Chạy ứng dụng
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
