# q-reserve Setup Guide

This guide will help you set up and run the q-reserve helpdesk/ticketing system.

## Prerequisites

- Python 3.11+ (you have 3.13.5 ✓)
- PostgreSQL 13+
- Redis (for background jobs)
- Docker & Docker Compose (optional)

## Quick Start

### Option 1: Local Development

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   # or
   source venv/bin/activate  # On Unix/Linux
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**:
   ```bash
   copy env.example .env
   # Edit .env with your database and email settings
   ```

4. **Start PostgreSQL and Redis**:
   ```bash
   docker-compose up -d postgres redis
   ```

5. **Run database migrations**:
   ```bash
   alembic upgrade head
   ```

6. **Seed initial data**:
   ```bash
   python scripts/seed_data.py
   ```

7. **Start the application**:
   ```bash
   python run.py
   # or
   uvicorn backend.app.main:app --reload
   ```

8. **Start Celery worker** (in another terminal):
   ```bash
   celery -A backend.app.core.celery worker --loglevel=info
   ```

### Option 2: Docker Development

1. **Start all services**:
   ```bash
   docker-compose up -d
   ```

2. **Seed initial data**:
   ```bash
   docker-compose exec app python scripts/seed_data.py
   ```

## Access the Application

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Admin Interface**: http://localhost:8000/admin

## Default Credentials

- **Admin User**: admin@qreserve.com / admin123
- **Default Categories**: General Support, Technical Issue, Feature Request, Bug Report, Account Issue

## Development Commands

```bash
# Run tests
pytest

# Run linting
black backend/
isort backend/
ruff check backend/

# Format code
make format

# Run with coverage
pytest --cov=backend

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

## Project Structure

```
q-reserve/
├── backend/                 # Backend application
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── core/           # Configuration & utilities
│   │   ├── db/             # Database setup
│   │   ├── models/         # SQLModel models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── templates/      # Jinja2 templates
│   │   └── static/         # Static files
│   ├── migrations/         # Alembic migrations
│   └── tests/              # Test suite
├── scripts/                # Utility scripts
├── uploads/                # File uploads
├── docker-compose.yml      # Development Docker setup
├── docker-compose.prod.yml # Production Docker setup
├── requirements.txt        # Python dependencies
├── alembic.ini           # Database migrations
└── README.md             # Project documentation
```

## Features Implemented

### ✅ Core Features
- [x] User registration/login with JWT authentication
- [x] Role-based access control (end_user, agent, admin)
- [x] Ticket creation and management
- [x] Threaded comments on tickets
- [x] Upvote/downvote system
- [x] Category management
- [x] Email notifications (async with Celery)
- [x] File attachments
- [x] Dark/light mode toggle
- [x] Advanced filtering and search
- [x] Responsive design with Tailwind CSS

### ✅ Technical Features
- [x] FastAPI backend with automatic API docs
- [x] PostgreSQL database with SQLModel ORM
- [x] Alembic migrations
- [x] JWT authentication with refresh tokens
- [x] Background job processing with Celery + Redis
- [x] File upload handling
- [x] Comprehensive test suite
- [x] Code quality tools (black, isort, ruff)
- [x] Pre-commit hooks
- [x] GitHub Actions CI/CD
- [x] Docker containerization
- [x] Production-ready configuration

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/refresh` - Refresh JWT token
- `GET /api/v1/auth/me` - Get current user profile

### Tickets
- `GET /api/v1/tickets` - List tickets (with filtering)
- `POST /api/v1/tickets` - Create ticket
- `GET /api/v1/tickets/{id}` - Get ticket details
- `PATCH /api/v1/tickets/{id}` - Update ticket
- `POST /api/v1/tickets/{id}/vote` - Vote on ticket

### Comments
- `POST /api/v1/comments` - Create comment
- `GET /api/v1/comments/ticket/{ticket_id}` - Get ticket comments

### Categories (Admin)
- `GET /api/v1/categories` - List categories
- `POST /api/v1/categories` - Create category
- `PATCH /api/v1/categories/{id}` - Update category
- `DELETE /api/v1/categories/{id}` - Delete category

### Users (Admin)
- `GET /api/v1/users` - List users
- `PATCH /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

## Environment Variables

Copy `env.example` to `.env` and configure:

```bash
# Database
DATABASE_URL=postgresql://qreserve:password@localhost:5432/qreserve
REDIS_URL=redis://localhost:6379

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email
SMTP_HOST=localhost
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
FROM_EMAIL=noreply@qreserve.com

# File Storage
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif,pdf,doc,docx,txt
```

## Troubleshooting

### Common Issues

1. **Database connection error**:
   - Ensure PostgreSQL is running
   - Check DATABASE_URL in .env
   - Run `alembic upgrade head`

2. **Redis connection error**:
   - Ensure Redis is running
   - Check REDIS_URL in .env

3. **Import errors**:
   - Ensure you're in the correct directory
   - Check Python path includes project root
   - Verify all dependencies are installed

4. **Email not sending**:
   - Configure SMTP settings in .env
   - Ensure Celery worker is running
   - Check email service logs

### Development Tips

- Use `make help` to see all available commands
- Run `make setup` for complete initial setup
- Use `docker-compose logs` to view service logs
- Check `/docs` for interactive API documentation

## Next Steps

1. **Customize the application**:
   - Modify templates in `backend/app/templates/`
   - Add custom CSS in `backend/app/static/`
   - Extend API endpoints in `backend/app/api/v1/`

2. **Deploy to production**:
   - Set up production environment variables
   - Configure SSL certificates
   - Set up monitoring and logging
   - Use `docker-compose.prod.yml`

3. **Add advanced features**:
   - Real-time updates with WebSockets
   - Advanced reporting and analytics
   - Multi-language support
   - Two-factor authentication

## Support

For issues and questions:
- Check the API documentation at `/docs`
- Review the test suite for usage examples
- Check the GitHub repository for updates 