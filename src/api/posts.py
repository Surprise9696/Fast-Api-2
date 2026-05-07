from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from src.api.depends import get_post_repository, get_category_repository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.infrastructure.sqlite.repositories.categories import CategoryRepository
from src.schemas.posts import Post, PostCreate, PostUpdate, PostListResponse

router = APIRouter(prefix="/posts", tags=["posts"])

@router.get("/", response_model=List[PostListResponse])
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    category_id: Optional[int] = None,
    repo: PostRepository = Depends(get_post_repository)
):
    posts = repo.get_published(skip=skip, limit=limit, category_id=category_id)
    
    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "text": post.text,
            "pub_date": post.pub_date,
            "author_id": post.author_id,
            "category_id": post.category_id,
            "image": post.image,
        })
    return result

@router.get("/{post_id}", response_model=Post)
async def get_post(
    post_id: int,
    repo: PostRepository = Depends(get_post_repository)
):
    post = repo.get_by_id_with_relations(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    return post

@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    repo: PostRepository = Depends(get_post_repository),
    category_repo: CategoryRepository = Depends(get_category_repository)
):
    category = category_repo.get_by_id(post_data.category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Указанная категория не существует"
        )
    
    created_post = repo.create(**post_data.model_dump())
    
    post_with_relations = repo.get_by_id_with_relations(created_post.id)
    
    if not post_with_relations:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден после создания"
        )
    
    return post_with_relations

@router.put("/{post_id}", response_model=Post)
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    repo: PostRepository = Depends(get_post_repository)
):
    existing = repo.get_by_id(post_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    
    update_data = post_data.model_dump(exclude_unset=True)
    updated = repo.update(post_id, **update_data)
    return updated

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    repo: PostRepository = Depends(get_post_repository)
):
    deleted = repo.delete(post_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    return None

@router.get("/search/", response_model=List[PostListResponse])
async def search_posts(
    q: str,
    repo: PostRepository = Depends(get_post_repository)
):
    posts = repo.search(q)
    
    result = []
    for post in posts:
        result.append({
            "id": post.id,
            "title": post.title,
            "pub_date": post.pub_date,
            "author": post.author,
            "category": post.category,
            "image": post.image,
            "comment_count": len(post.comments) if hasattr(post, 'comments') else 0
        })
    return result