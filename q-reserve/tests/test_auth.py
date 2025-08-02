import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool

from backend.app.main import app
from backend.app.core.config import settings
from backend.app.db.session import get_session
from backend.app.models.user import User
from backend.app.core.security import get_password_hash


# Create test database
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "password": "testpassword",
        "full_name": "Test User",
    }


def test_register_user(client, test_user):
    """Test user registration."""
    response = client.post("/api/v1/auth/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == test_user["email"]
    assert data["full_name"] == test_user["full_name"]
    assert "id" in data


def test_login_user(client, test_user):
    """Test user login."""
    # First register the user
    client.post("/api/v1/auth/register", json=test_user)
    
    # Then try to login
    response = client.post("/api/v1/auth/login", json={
        "email": test_user["email"],
        "password": test_user["password"],
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client):
    """Test login with invalid credentials."""
    response = client.post("/api/v1/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "wrongpassword",
    })
    assert response.status_code == 401 