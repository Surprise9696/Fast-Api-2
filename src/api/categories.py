from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.api.depends import get_category_repository
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["categories"])

@router.get("/", response_model=List[Category])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    only_published: bool = True,
    repo: CategoryRepository = Depends(get_category_repository)
):
    if only_published:
        return repo.get_published(skip=skip, limit=limit)
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{category_id}", response_model=Category)
async def get_category(
    category_id: int,
    repo: CategoryRepository = Depends(get_category_repository)
):
    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return category

@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    category_data: CategoryCreate,
    repo: CategoryRepository = Depends(get_category_repository)
):
    existing = repo.get_by_slug(category_data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Категория с таким slug уже существует"
        )
    
    return repo.create(**category_data.model_dump())

@router.put("/{category_id}", response_model=Category)
async def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    repo: CategoryRepository = Depends(get_category_repository)
):
    existing = repo.get_by_id(category_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    
    if category_data.slug and category_data.slug != existing.slug:
        slug_exists = repo.get_by_slug(category_data.slug)
        if slug_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Категория с таким slug уже существует"
            )
    
    update_data = category_data.model_dump(exclude_unset=True)
    updated = repo.update(category_id, **update_data)
    return updated

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    repo: CategoryRepository = Depends(get_category_repository)
):
    deleted = repo.delete(category_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Категория не найдена"
        )
    return None