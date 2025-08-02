#!/usr/bin/env python3
"""
Seed script for q-reserve database.
Creates admin user and default categories.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.db.session import engine
from backend.app.db.init_db import init_db
from backend.app.core.config import settings


def main():
    """Run the seed script."""
    print("Seeding database...")
    
    try:
        # Initialize database with seed data
        init_db()
        print("Database seeded successfully!")
        print("\nDefault admin credentials:")
        print("Email: admin@qreserve.com")
        print("Password: admin123")
        print("\nDefault categories created:")
        print("- General Support")
        print("- Technical Issue")
        print("- Feature Request")
        print("- Bug Report")
        print("- Account Issue")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 