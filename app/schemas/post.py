from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class PostBase(BaseModel):
    """Base post schema"""
    title: str
    content: str
    published: bool = False


class PostCreate(PostBase):
    """Schema for creating a post"""
    pass


class PostUpdate(BaseModel):
    """Schema for updating a post"""
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None


class Post(PostBase):
    """Public post schema"""
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PostWithAuthor(Post):
    """Post schema with author information"""
    author: dict

    model_config = ConfigDict(from_attributes=True)