from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import User, UserUpdate
from app.models.user import User as UserModel
from app.crud.user import get_user, get_users, update_user, delete_user
from app.utils.dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User)
def read_current_user(current_user: UserModel = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user


@router.get("/", response_model=List[User])
def read_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_active_user)
):
    """Get list of users (protected route)"""
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=User)
def read_user(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_active_user)
):
    """Get user by ID"""
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.put("/{user_id}", response_model=User)
def update_user_route(
        user_id: int,
        user_update: UserUpdate,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_active_user)
):
    """Update user (only own profile)"""
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    db_user = update_user(db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_route(
        user_id: int,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_active_user)
):
    """Delete user (only own profile or superuser)"""
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user"
        )

    success = delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return None