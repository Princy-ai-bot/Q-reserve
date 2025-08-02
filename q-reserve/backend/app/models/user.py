from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr


class UserRole(str, Enum):
    end_user = "end_user"
    agent = "agent"
    admin = "admin"


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    full_name: str
    role: UserRole = UserRole.end_user
    is_active: bool = True
    dark_mode: bool = False


class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    tickets: list["Ticket"] = Relationship(back_populates="owner")
    assigned_tickets: list["Ticket"] = Relationship(back_populates="assignee")
    comments: list["Comment"] = Relationship(back_populates="author")
    votes: list["Vote"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    dark_mode: Optional[bool] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime
    updated_at: datetime 