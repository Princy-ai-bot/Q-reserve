from sqlmodel import Session, select
from ..models.user import User, UserRole
from ..models.category import Category
from ..core.security import get_password_hash
from .session import engine


def init_db():
    """Initialize database with seed data."""
    with Session(engine) as session:
        # Create admin user if not exists
        admin_user = session.exec(
            select(User).where(User.email == "admin@qreserve.com")
        ).first()
        
        if not admin_user:
            admin_user = User(
                email="admin@qreserve.com",
                hashed_password=get_password_hash("admin123"),
                full_name="System Administrator",
                role=UserRole.admin,
                is_active=True,
            )
            session.add(admin_user)
            session.commit()
            print("Created admin user: admin@qreserve.com / admin123")
        
        # Create default categories
        default_categories = [
            "General Support",
            "Technical Issue",
            "Feature Request",
            "Bug Report",
            "Account Issue",
        ]
        
        for category_name in default_categories:
            existing_category = session.exec(
                select(Category).where(Category.name == category_name)
            ).first()
            
            if not existing_category:
                category = Category(
                    name=category_name,
                    description=f"Default category for {category_name.lower()}",
                    is_active=True,
                )
                session.add(category)
        
        session.commit()
        print("Database initialized with seed data") 