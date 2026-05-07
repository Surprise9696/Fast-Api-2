from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.api.depends import get_user_repository
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.users import User, UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    repo: UserRepository = Depends(get_user_repository)
):
    return repo.get_all(skip=skip, limit=limit)

@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository)
):
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user

@router.get("/username/{username}", response_model=User)
async def get_user_by_username(
    username: str,
    repo: UserRepository = Depends(get_user_repository)
):
    user = repo.get_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    repo: UserRepository = Depends(get_user_repository)
):
    existing_username = repo.get_by_username(user_data.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )
    
    existing_email = repo.get_by_email(user_data.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )
    
    created_user = repo.create(**user_data.model_dump())
    
    return created_user

@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    repo: UserRepository = Depends(get_user_repository)
):
    existing = repo.get_by_id(user_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    update_data = user_data.model_dump(exclude_unset=True)
    return repo.update(user_id, **update_data)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository)
):
    deleted = repo.delete(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return None