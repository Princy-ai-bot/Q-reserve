from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from ...core.dependencies import get_current_active_user, get_session
from ...models.user import User
from ...models.ticket import Ticket
from ...models.comment import Comment, CommentCreate, CommentRead
from ...services.notification_service import send_comment_notification_email

router = APIRouter()


@router.post("/", response_model=CommentRead)
async def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Create a new comment on a ticket."""
    # Validate ticket exists
    ticket = session.exec(
        select(Ticket).where(Ticket.id == comment_data.ticket_id)
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    # Check access permissions
    if current_user.role == "end_user" and ticket.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to comment on this ticket",
        )
    
    # Validate parent comment if provided
    if comment_data.parent_id:
        parent_comment = session.exec(
            select(Comment).where(Comment.id == comment_data.parent_id)
        ).first()
        if not parent_comment or parent_comment.ticket_id != comment_data.ticket_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid parent comment",
            )
    
    # Create comment
    comment = Comment(
        **comment_data.dict(),
        author_id=current_user.id,
    )
    
    session.add(comment)
    session.commit()
    session.refresh(comment)
    
    # Send notification to ticket owner if commenter is not the owner
    if comment.author_id != ticket.owner_id:
        send_comment_notification_email.delay(
            to_email=ticket.owner.email,
            ticket_id=ticket.id,
            subject=ticket.subject,
            commenter_name=current_user.full_name,
        )
    
    return comment


@router.get("/ticket/{ticket_id}", response_model=List[CommentRead])
async def get_ticket_comments(
    ticket_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Get all comments for a ticket."""
    # Validate ticket exists
    ticket = session.exec(
        select(Ticket).where(Ticket.id == ticket_id)
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    # Check access permissions
    if current_user.role == "end_user" and ticket.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this ticket",
        )
    
    # Get comments (only top-level comments, replies will be included in the response)
    comments = session.exec(
        select(Comment)
        .where(Comment.ticket_id == ticket_id, Comment.parent_id.is_(None))
        .order_by(Comment.created_at.asc())
    ).all()
    
    return comments


@router.get("/{comment_id}", response_model=CommentRead)
async def get_comment(
    comment_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Get a specific comment."""
    comment = session.exec(
        select(Comment).where(Comment.id == comment_id)
    ).first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )
    
    # Check access permissions
    if current_user.role == "end_user" and comment.ticket.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this comment",
        )
    
    return comment 