import asyncio
from typing import List, Optional
from aiosmtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .config import settings


class EmailService:
    def __init__(self):
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.from_email = settings.from_email
        self.from_name = settings.from_name
    
    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """Send email asynchronously."""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.from_name} <{self.from_email}>"
            message["To"] = to_email
            
            if text_content:
                text_part = MIMEText(text_content, "plain")
                message.attach(text_part)
            
            html_part = MIMEText(html_content, "html")
            message.attach(html_part)
            
            smtp = SMTP(
                hostname=self.smtp_host,
                port=self.smtp_port,
                use_tls=True,
                username=self.smtp_username,
                password=self.smtp_password,
            )
            
            await smtp.connect()
            if self.smtp_username and self.smtp_password:
                await smtp.login(self.smtp_username, self.smtp_password)
            
            await smtp.send_message(message)
            await smtp.quit()
            
            return True
        except Exception as e:
            print(f"Email sending failed: {e}")
            return False
    
    async def send_ticket_created_notification(
        self, to_email: str, ticket_id: int, subject: str, owner_name: str
    ):
        """Send notification when ticket is created."""
        html_content = f"""
        <html>
            <body>
                <h2>New Ticket Created</h2>
                <p>Hello {owner_name},</p>
                <p>Your ticket has been created successfully.</p>
                <p><strong>Ticket ID:</strong> #{ticket_id}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p>You can view your ticket at: {settings.base_url}/tickets/{ticket_id}</p>
                <br>
                <p>Thank you for using q-reserve!</p>
            </body>
        </html>
        """
        
        await self.send_email(
            to_email=to_email,
            subject=f"Ticket #{ticket_id} Created - {subject}",
            html_content=html_content,
        )
    
    async def send_ticket_updated_notification(
        self, to_email: str, ticket_id: int, subject: str, status: str
    ):
        """Send notification when ticket status is updated."""
        html_content = f"""
        <html>
            <body>
                <h2>Ticket Status Updated</h2>
                <p>Your ticket status has been updated.</p>
                <p><strong>Ticket ID:</strong> #{ticket_id}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>New Status:</strong> {status}</p>
                <p>You can view your ticket at: {settings.base_url}/tickets/{ticket_id}</p>
                <br>
                <p>Thank you for using q-reserve!</p>
            </body>
        </html>
        """
        
        await self.send_email(
            to_email=to_email,
            subject=f"Ticket #{ticket_id} Status Updated - {subject}",
            html_content=html_content,
        )
    
    async def send_comment_notification(
        self, to_email: str, ticket_id: int, subject: str, commenter_name: str
    ):
        """Send notification when new comment is added."""
        html_content = f"""
        <html>
            <body>
                <h2>New Comment on Your Ticket</h2>
                <p>Someone has commented on your ticket.</p>
                <p><strong>Ticket ID:</strong> #{ticket_id}</p>
                <p><strong>Subject:</strong> {subject}</p>
                <p><strong>Commenter:</strong> {commenter_name}</p>
                <p>You can view the comment at: {settings.base_url}/tickets/{ticket_id}</p>
                <br>
                <p>Thank you for using q-reserve!</p>
            </body>
        </html>
        """
        
        await self.send_email(
            to_email=to_email,
            subject=f"New Comment on Ticket #{ticket_id} - {subject}",
            html_content=html_content,
        )


email_service = EmailService() 