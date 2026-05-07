from fastapi import APIRouter, FastAPI, HTTPException
from typing import List
from src.schemas.category import Category, CategoryCreate, CategoryUpdate

app = FastAPI()

router = APIRouter()

posts_db = {}
categories_db = {}
comments_db = {}
locations_db = {}


@router.get("/categories/", response_model=List[Category])
async def get_categories():
    return list(categories_db.values())

@router.post("/categories/", response_model=Category)
async def create_category(category: CategoryCreate):
    new_category = Category(id=len(categories_db) + 1, **category.model_dump())
    categories_db[new_category.id] = new_category
    return new_category

@router.put("/categories/{category_id}", response_model=Category)
async def update_category(category_id: int, category: CategoryUpdate):
    if category_id not in categories_db:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    existing_category = categories_db[category_id]
    update_data = category.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(existing_category, field, value)
    
    categories_db[category_id] = existing_category
    return existing_category

@router.delete("/categories/{category_id}")
async def delete_category(category_id: int):
    if category_id not in categories_db:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    posts_in_category = [p for p in posts_db.values() if p.category.id == category_id]
    if posts_in_category:
        raise HTTPException(
            status_code=400, 
            detail="Невозможно удалить категорию, в которой есть посты"
        )
    
    del categories_db[category_id]
    return {"message": "Категория успешно удалена"}

