from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.post import Post, PostCreate, PostUpdate
from app.models.user import User
from app.crud.post import (
    get_post,
    get_posts,
    get_published_posts,
    get_posts_by_user,
    create_post,
    update_post,
    delete_post
)
from app.utils.dependencies import get_current_active_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=Post, status_code=status.HTTP_201_CREATED)
def create_new_post(
        post: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Create a new blog post"""
    return create_post(db=db, post=post, user_id=current_user.id)


@router.get("/", response_model=List[Post])
def read_posts(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    """Get all published posts (public)"""
    posts = get_published_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/all", response_model=List[Post])
def read_all_posts(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get all posts including unpublished (protected)"""
    posts = get_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/my-posts", response_model=List[Post])
def read_my_posts(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Get current user's posts"""
    posts = get_posts_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}", response_model=Post)
def read_post(
        post_id: int,
        db: Session = Depends(get_db)
):
    """Get post by ID (public if published)"""
    db_post = get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Only show published posts to public
    if not db_post.published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    return db_post


@router.put("/{post_id}", response_model=Post)
def update_post_route(
        post_id: int,
        post_update: PostUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Update post (only author can update)"""
    db_post = get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check if current user is the author
    if db_post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post"
        )

    updated_post = update_post(db, post_id=post_id, post_update=post_update)
    return updated_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_route(
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    """Delete post (only author can delete)"""
    db_post = get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    # Check if current user is the author
    if db_post.author_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    success = delete_post(db, post_id=post_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return None