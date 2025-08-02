from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class CategoryBase(SQLModel):
    name: str = Field(unique=True, index=True)
    description: Optional[str] = None
    is_active: bool = True


class Category(CategoryBase, table=True):
    __tablename__ = "categories"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tickets: list["Ticket"] = Relationship(back_populates="category")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class CategoryRead(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime 