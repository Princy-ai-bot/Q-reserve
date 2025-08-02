from ..core.celery import celery
from ..core.email import email_service


@celery.task
def send_ticket_created_email(to_email: str, ticket_id: int, subject: str, owner_name: str):
    """Send ticket created notification email."""
    import asyncio
    
    async def send_email():
        await email_service.send_ticket_created_notification(
            to_email=to_email,
            ticket_id=ticket_id,
            subject=subject,
            owner_name=owner_name,
        )
    
    asyncio.run(send_email())


@celery.task
def send_ticket_updated_email(to_email: str, ticket_id: int, subject: str, status: str):
    """Send ticket updated notification email."""
    import asyncio
    
    async def send_email():
        await email_service.send_ticket_updated_notification(
            to_email=to_email,
            ticket_id=ticket_id,
            subject=subject,
            status=status,
        )
    
    asyncio.run(send_email())


@celery.task
def send_comment_notification_email(to_email: str, ticket_id: int, subject: str, commenter_name: str):
    """Send comment notification email."""
    import asyncio
    
    async def send_email():
        await email_service.send_comment_notification(
            to_email=to_email,
            ticket_id=ticket_id,
            subject=subject,
            commenter_name=commenter_name,
        )
    
    asyncio.run(send_email()) 