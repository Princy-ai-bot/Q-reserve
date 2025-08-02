from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class TicketStatus(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class TicketPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class TicketBase(SQLModel):
    subject: str = Field(index=True)
    description: str
    status: TicketStatus = TicketStatus.open
    priority: TicketPriority = TicketPriority.medium
    category_id: Optional[int] = Field(default=None, foreign_key="categories.id")
    assignee_id: Optional[int] = Field(default=None, foreign_key="users.id")


class Ticket(TicketBase, table=True):
    __tablename__ = "tickets"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    owner: "User" = Relationship(back_populates="tickets", foreign_keys=[owner_id])
    assignee: Optional["User"] = Relationship(back_populates="assigned_tickets", foreign_keys=[assignee_id])
    category: Optional["Category"] = Relationship(back_populates="tickets")
    comments: list["Comment"] = Relationship(back_populates="ticket")
    votes: list["Vote"] = Relationship(back_populates="ticket")
    attachments: list["Attachment"] = Relationship(back_populates="ticket")


class TicketCreate(TicketBase):
    pass


class TicketUpdate(SQLModel):
    subject: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None
    category_id: Optional[int] = None
    assignee_id: Optional[int] = None


class TicketRead(TicketBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    last_activity: datetime
    owner: "UserRead"
    assignee: Optional["UserRead"] = None
    category: Optional["CategoryRead"] = None
    comment_count: int = 0
    vote_score: int = 0
    user_vote: Optional[str] = None  # "up" or "down" or None


class TicketList(TicketBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    last_activity: datetime
    owner: "UserRead"
    assignee: Optional["UserRead"] = None
    category: Optional["CategoryRead"] = None
    comment_count: int = 0
    vote_score: int = 0 