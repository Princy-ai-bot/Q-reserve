from datetime import datetime
from enum import Enum
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class VoteType(str, Enum):
    up = "up"
    down = "down"


class VoteBase(SQLModel):
    ticket_id: int = Field(foreign_key="tickets.id")
    vote_type: VoteType


class Vote(VoteBase, table=True):
    __tablename__ = "votes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    user: "User" = Relationship(back_populates="votes")
    ticket: "Ticket" = Relationship(back_populates="votes")


class VoteCreate(VoteBase):
    pass


class VoteUpdate(SQLModel):
    vote_type: VoteType


class VoteRead(VoteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime 