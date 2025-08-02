from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

from .core.config import settings
from .db.session import init
from .api.v1 import auth, tickets, comments, categories, users

# Create FastAPI app
app = FastAPI(
    title="q-reserve",
    description="A lightweight helpdesk/ticketing system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(tickets.router, prefix="/api/v1/tickets", tags=["tickets"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["categories"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

# Setup static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Create uploads directory if it doesn't exist
os.makedirs(settings.upload_dir, exist_ok=True)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init()


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main application page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "q-reserve"} 