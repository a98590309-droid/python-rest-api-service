from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

app = FastAPI(
    title="Item Store API",
    description="REST API featuring typed Pydantic models, input validation, and auto-generated Swagger docs.",
    version="1.0.0"
)

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)
    in_stock: bool = Field(default=True)

class ItemResponse(ItemCreate):
    id: int

db: dict[int, ItemResponse] = {}
counter: int = 1

@app.get("/items", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
def get_all_items():
    return list(db.values())

@app.get("/items/{item_id}", response_model=ItemResponse, status_code=status.HTTP_200_OK)
def get_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return db[item_id]

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemCreate):
    global counter
    new_item = ItemResponse(id=counter, **item.model_dump())
    db[counter] = new_item
    counter += 1
    return new_item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del db[item_id]
    return None
