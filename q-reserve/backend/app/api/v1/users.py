from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ...core.dependencies import require_admin, get_session
from ...models.user import User, UserUpdate, UserRead, UserRole

router = APIRouter()


@router.get("/", response_model=List[UserRead])
async def list_users(
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """List all users (admin only)."""
    users = session.exec(
        select(User).order_by(User.created_at.desc())
    ).all()
    
    return users


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Get a specific user (admin only)."""
    user = session.exec(
        select(User).where(User.id == user_id)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return user


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Update a user (admin only)."""
    user = session.exec(
        select(User).where(User.id == user_id)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if email already exists (if changing email)
    if user_update.email and user_update.email != user.email:
        existing_user = session.exec(
            select(User).where(User.email == user_update.email)
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists",
            )
    
    # Update user
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Delete a user (admin only)."""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself",
        )
    
    user = session.exec(
        select(User).where(User.id == user_id)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Check if user has tickets
    from ...models.ticket import Ticket
    tickets_count = session.exec(
        select(Ticket).where(Ticket.owner_id == user_id)
    ).all()
    
    if tickets_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete user with existing tickets",
        )
    
    session.delete(user)
    session.commit()
    
    return {"message": "User deleted successfully"} 