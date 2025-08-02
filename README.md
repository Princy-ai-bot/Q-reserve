000# Q-reserve

# q-reserve

A lightweight, production-ready helpdesk/ticketing system built with FastAPI, PostgreSQL, and Tailwind CSS.

## Features

- **Role-based access control**: End users, agents, and admins
- **Ticket management**: Create, update, and track support tickets
- **Threaded comments**: Full conversation history on tickets
- **Voting system**: Upvote/downvote tickets
- **Email notifications**: Async notifications for ticket events
- **File attachments**: Secure file upload and storage
- **Dark/Light mode**: User-persisted theme preference
- **Advanced filtering**: Search, sort, and filter tickets
- **Responsive design**: Mobile-friendly interface

## Tech Stack

- **Backend**: FastAPI, SQLModel, PostgreSQL
- **Authentication**: JWT with refresh tokens
- **Frontend**: Tailwind CSS, HTMX, Jinja2 templates
- **Background Jobs**: Celery with Redis
- **Testing**: pytest, HTTPX
- **Linting**: black, isort, ruff
- **CI/CD**: GitHub Actions

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Redis (for background jobs)
- Docker & Docker Compose (optional)

### Development Setup

1. **Clone and setup environment**:
   ```bash
   git clone <repository-url>
   cd q-reserve
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment configuration**:
   ```bash
   cp .env.example .env
   # Edit .env with your database and email settings
   ```

3. **Database setup**:
   ```bash
   # Start PostgreSQL and Redis (if using Docker)
   docker-compose up -d postgres redis
   
   # Run migrations
   alembic upgrade head
   
   # Seed initial data
   python scripts/seed_data.py
   ```

4. **Start development server**:
   ```bash
   uvicorn backend.app.main:app --reload
   ```

5. **Access the application**:
   - Web interface: http://localhost:8000
   - API docs: http://localhost:8000/docs
   - Admin interface: http://localhost:8000/admin

### Docker Setup

```bash
docker-compose up -d
```

## Development

### Code Quality

```bash
# Install pre-commit hooks
pre-commit install

# Run linting
black backend/
isort backend/
ruff check backend/

# Run tests
pytest
```

### Database Migrations

```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend

# Run specific test file
pytest tests/test_auth.py
```

## API Documentation

The API is automatically documented at `/docs` (Swagger UI) and `/redoc` (ReDoc).

### Key Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/tickets` - List tickets
- `POST /api/v1/tickets` - Create ticket
- `GET /api/v1/tickets/{id}` - Get ticket details
- `POST /api/v1/tickets/{id}/comments` - Add comment
- `POST /api/v1/tickets/{id}/vote` - Vote on ticket

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://postgres:Mohitraj%401606@localhost:5432/q_reserv` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `SECRET_KEY` | JWT secret key | `xpEiN4OrosyZbUTf3D7EbdT4l1ZcvtZw7-A59anO5xU` |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT access token expiry | `30` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | JWT refresh token expiry | `7` |
| `SMTP_HOST` | SMTP server host | `localhost` |
| `SMTP_PORT` | SMTP server port | `587` |
| `SMTP_USERNAME` | SMTP username | `` |
| `SMTP_PASSWORD` | SMTP password | `` |
| `FROM_EMAIL` | Default sender email | `noreply@qreserve.com` |

## Deployment

### Production Checklist

- [ ] Set production environment variables
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper database backups
- [ ] Configure email service (SendGrid/Mailgun)
- [ ] Set up monitoring and logging
- [ ] Configure file storage (S3-compatible)
- [ ] Set up CI/CD pipeline

### Docker Production

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

MIT License - see LICENSE file for details. 
