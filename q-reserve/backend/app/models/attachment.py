from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class AttachmentBase(SQLModel):
    filename: str
    file_path: str
    file_size: int
    mime_type: str
    ticket_id: int = Field(foreign_key="tickets.id")


class Attachment(AttachmentBase, table=True):
    __tablename__ = "attachments"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    uploaded_by_id: int = Field(foreign_key="users.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    uploaded_by: "User" = Relationship()
    ticket: "Ticket" = Relationship(back_populates="attachments")


class AttachmentCreate(AttachmentBase):
    pass


class AttachmentRead(AttachmentBase):
    id: int
    uploaded_by_id: int
    created_at: datetime
    uploaded_by: "UserRead" 