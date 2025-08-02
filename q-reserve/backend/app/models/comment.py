from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class CommentBase(SQLModel):
    content: str
    ticket_id: int = Field(foreign_key="tickets.id")
    parent_id: Optional[int] = Field(default=None, foreign_key="comments.id")


class Comment(CommentBase, table=True):
    __tablename__ = "comments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    author: "User" = Relationship(back_populates="comments")
    ticket: "Ticket" = Relationship(back_populates="comments")
    parent: Optional["Comment"] = Relationship(
        back_populates="replies",
        foreign_keys=[parent_id],
        sa_relationship_kwargs={"remote_side": "Comment.id"}
    )
    replies: list["Comment"] = Relationship(
        back_populates="parent",
        foreign_keys=[parent_id]
    )


class CommentCreate(CommentBase):
    pass


class CommentUpdate(SQLModel):
    content: str


class CommentRead(CommentBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    author: "UserRead"
    replies: list["CommentRead"] = [] 