from sqlalchemy.orm import Session
from typing import Optional
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate


def get_post(db: Session, post_id: int) -> Optional[Post]:
    """Get post by ID"""
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts(db: Session, skip: int = 0, limit: int = 100) -> list[Post]:
    """Get list of all posts"""
    return db.query(Post).offset(skip).limit(limit).all()


def get_published_posts(db: Session, skip: int = 0, limit: int = 100) -> list[Post]:
    """Get list of published posts"""
    return db.query(Post).filter(Post.published == True).offset(skip).limit(limit).all()


def get_posts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> list[Post]:
    """Get posts by user"""
    return db.query(Post).filter(Post.author_id == user_id).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate, user_id: int) -> Post:
    """Create new post"""
    db_post = Post(
        **post.model_dump(),
        author_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, post_id: int, post_update: PostUpdate) -> Optional[Post]:
    """Update post"""
    db_post = get_post(db, post_id)
    if not db_post:
        return None

    update_data = post_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_post, field, value)

    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: int) -> bool:
    """Delete post"""
    db_post = get_post(db, post_id)
    if not db_post:
        return False

    db.delete(db_post)
    db.commit()
    return True