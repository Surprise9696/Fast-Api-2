from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from src.api.depends import get_comment_repository, get_post_repository
from src.infrastructure.sqlite.repositories.comments import CommentRepository
from src.infrastructure.sqlite.repositories.posts import PostRepository
from src.schemas.comment import Comment, CommentCreate, CommentUpdate

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/post/{post_id}", response_model=List[Comment])
async def get_post_comments(
    post_id: int,
    repo: CommentRepository = Depends(get_comment_repository)
):
    return repo.get_by_post(post_id)

@router.post("/", response_model=Comment, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    repo: CommentRepository = Depends(get_comment_repository),
    post_repo: PostRepository = Depends(get_post_repository)
):
    post = post_repo.get_by_id(comment_data.post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден"
        )
    
    return repo.create(**comment_data.model_dump())

@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    repo: CommentRepository = Depends(get_comment_repository)
):
    existing = repo.get_by_id(comment_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комментарий не найден"
        )
    
    update_data = comment_data.model_dump(exclude_unset=True)
    return repo.update(comment_id, **update_data)

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    repo: CommentRepository = Depends(get_comment_repository)
):
    deleted = repo.delete(comment_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Комментарий не найден"
        )
    return None