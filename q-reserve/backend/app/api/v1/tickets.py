from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session, select, func
from ...core.dependencies import get_current_active_user, require_agent_or_admin, get_session
from ...models.user import User, UserRole
from ...models.ticket import Ticket, TicketCreate, TicketUpdate, TicketRead, TicketList, TicketStatus
from ...models.category import Category
from ...models.vote import Vote, VoteType
from ...services.notification_service import send_ticket_created_email, send_ticket_updated_email

router = APIRouter()


@router.post("/", response_model=TicketRead)
async def create_ticket(
    ticket_data: TicketCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Create a new ticket."""
    # Validate category exists
    if ticket_data.category_id:
        category = session.exec(
            select(Category).where(Category.id == ticket_data.category_id)
        ).first()
        if not category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid category ID",
            )
    
    # Create ticket
    ticket = Ticket(
        **ticket_data.dict(),
        owner_id=current_user.id,
    )
    
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    
    # Send notification email
    send_ticket_created_email.delay(
        to_email=current_user.email,
        ticket_id=ticket.id,
        subject=ticket.subject,
        owner_name=current_user.full_name,
    )
    
    return ticket


@router.get("/", response_model=List[TicketList])
async def list_tickets(
    status: Optional[TicketStatus] = Query(None),
    category_id: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    sort_by: str = Query("updated_at", regex="^(created_at|updated_at|subject|priority)$"),
    sort_order: str = Query("desc", regex="^(asc|desc)$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """List tickets with filtering and pagination."""
    # Build query
    query = select(Ticket)
    
    # Filter by user role
    if current_user.role == UserRole.end_user:
        query = query.where(Ticket.owner_id == current_user.id)
    
    # Apply filters
    if status:
        query = query.where(Ticket.status == status)
    if category_id:
        query = query.where(Ticket.category_id == category_id)
    if search:
        search_filter = f"%{search}%"
        query = query.where(
            (Ticket.subject.ilike(search_filter)) |
            (Ticket.description.ilike(search_filter))
        )
    
    # Apply sorting
    if sort_order == "desc":
        query = query.order_by(getattr(Ticket, sort_by).desc())
    else:
        query = query.order_by(getattr(Ticket, sort_by).asc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    
    tickets = session.exec(query).all()
    
    # Add related data
    result = []
    for ticket in tickets:
        # Get comment count
        comment_count = session.exec(
            select(func.count()).select_from(ticket.comments)
        ).first() or 0
        
        # Get vote score
        upvotes = session.exec(
            select(func.count()).select_from(ticket.votes).where(Vote.vote_type == VoteType.up)
        ).first() or 0
        downvotes = session.exec(
            select(func.count()).select_from(ticket.votes).where(Vote.vote_type == VoteType.down)
        ).first() or 0
        vote_score = upvotes - downvotes
        
        # Get user's vote
        user_vote = session.exec(
            select(Vote).where(Vote.ticket_id == ticket.id, Vote.user_id == current_user.id)
        ).first()
        user_vote_type = user_vote.vote_type if user_vote else None
        
        ticket_data = TicketList(
            id=ticket.id,
            subject=ticket.subject,
            description=ticket.description,
            status=ticket.status,
            priority=ticket.priority,
            category_id=ticket.category_id,
            assignee_id=ticket.assignee_id,
            owner_id=ticket.owner_id,
            created_at=ticket.created_at,
            updated_at=ticket.updated_at,
            last_activity=ticket.last_activity,
            owner=ticket.owner,
            assignee=ticket.assignee,
            category=ticket.category,
            comment_count=comment_count,
            vote_score=vote_score,
        )
        result.append(ticket_data)
    
    return result


@router.get("/{ticket_id}", response_model=TicketRead)
async def get_ticket(
    ticket_id: int,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Get ticket details."""
    ticket = session.exec(
        select(Ticket).where(Ticket.id == ticket_id)
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    # Check access permissions
    if current_user.role == UserRole.end_user and ticket.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this ticket",
        )
    
    # Get vote score and user vote
    upvotes = session.exec(
        select(func.count()).select_from(ticket.votes).where(Vote.vote_type == VoteType.up)
    ).first() or 0
    downvotes = session.exec(
        select(func.count()).select_from(ticket.votes).where(Vote.vote_type == VoteType.down)
    ).first() or 0
    vote_score = upvotes - downvotes
    
    user_vote = session.exec(
        select(Vote).where(Vote.ticket_id == ticket.id, Vote.user_id == current_user.id)
    ).first()
    user_vote_type = user_vote.vote_type if user_vote else None
    
    return TicketRead(
        id=ticket.id,
        subject=ticket.subject,
        description=ticket.description,
        status=ticket.status,
        priority=ticket.priority,
        category_id=ticket.category_id,
        assignee_id=ticket.assignee_id,
        owner_id=ticket.owner_id,
        created_at=ticket.created_at,
        updated_at=ticket.updated_at,
        last_activity=ticket.last_activity,
        owner=ticket.owner,
        assignee=ticket.assignee,
        category=ticket.category,
        comment_count=len(ticket.comments),
        vote_score=vote_score,
        user_vote=user_vote_type,
    )


@router.patch("/{ticket_id}", response_model=TicketRead)
async def update_ticket(
    ticket_id: int,
    ticket_update: TicketUpdate,
    current_user: User = Depends(require_agent_or_admin),
    session: Session = Depends(get_session),
):
    """Update ticket (agents and admins only)."""
    ticket = session.exec(
        select(Ticket).where(Ticket.id == ticket_id)
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    # Update ticket
    update_data = ticket_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)
    
    session.add(ticket)
    session.commit()
    session.refresh(ticket)
    
    # Send notification if status changed
    if "status" in update_data:
        send_ticket_updated_email.delay(
            to_email=ticket.owner.email,
            ticket_id=ticket.id,
            subject=ticket.subject,
            status=ticket.status,
        )
    
    return ticket


@router.post("/{ticket_id}/vote")
async def vote_ticket(
    ticket_id: int,
    vote_type: VoteType,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    """Vote on a ticket (upvote/downvote)."""
    ticket = session.exec(
        select(Ticket).where(Ticket.id == ticket_id)
    ).first()
    
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    # Check if user already voted
    existing_vote = session.exec(
        select(Vote).where(Vote.ticket_id == ticket_id, Vote.user_id == current_user.id)
    ).first()
    
    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # Remove vote if same type
            session.delete(existing_vote)
        else:
            # Change vote type
            existing_vote.vote_type = vote_type
            session.add(existing_vote)
    else:
        # Create new vote
        vote = Vote(
            ticket_id=ticket_id,
            user_id=current_user.id,
            vote_type=vote_type,
        )
        session.add(vote)
    
    session.commit()
    
    return {"message": "Vote updated successfully"} 