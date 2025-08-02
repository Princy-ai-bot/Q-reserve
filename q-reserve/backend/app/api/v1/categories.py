from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ...core.dependencies import require_admin, get_session
from ...models.user import User
from ...models.category import Category, CategoryCreate, CategoryUpdate, CategoryRead

router = APIRouter()


@router.post("/", response_model=CategoryRead)
async def create_category(
    category_data: CategoryCreate,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Create a new category (admin only)."""
    # Check if category name already exists
    existing_category = session.exec(
        select(Category).where(Category.name == category_data.name)
    ).first()
    
    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name already exists",
        )
    
    # Create category
    category = Category(**category_data.dict())
    session.add(category)
    session.commit()
    session.refresh(category)
    
    return category


@router.get("/", response_model=List[CategoryRead])
async def list_categories(
    session: Session = Depends(get_session),
):
    """List all active categories."""
    categories = session.exec(
        select(Category).where(Category.is_active == True).order_by(Category.name.asc())
    ).all()
    
    return categories


@router.get("/{category_id}", response_model=CategoryRead)
async def get_category(
    category_id: int,
    session: Session = Depends(get_session),
):
    """Get a specific category."""
    category = session.exec(
        select(Category).where(Category.id == category_id)
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    return category


@router.patch("/{category_id}", response_model=CategoryRead)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Update a category (admin only)."""
    category = session.exec(
        select(Category).where(Category.id == category_id)
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    # Check if new name conflicts with existing category
    if category_update.name and category_update.name != category.name:
        existing_category = session.exec(
            select(Category).where(Category.name == category_update.name)
        ).first()
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category name already exists",
            )
    
    # Update category
    update_data = category_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(category, field, value)
    
    session.add(category)
    session.commit()
    session.refresh(category)
    
    return category


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    current_user: User = Depends(require_admin),
    session: Session = Depends(get_session),
):
    """Delete a category (admin only)."""
    category = session.exec(
        select(Category).where(Category.id == category_id)
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    
    # Check if category has tickets
    from ...models.ticket import Ticket
    tickets_count = session.exec(
        select(Ticket).where(Ticket.category_id == category_id)
    ).all()
    
    if tickets_count:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete category with existing tickets",
        )
    
    session.delete(category)
    session.commit()
    
    return {"message": "Category deleted successfully"} 