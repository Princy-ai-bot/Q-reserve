#!/usr/bin/env python3
"""
Startup script for q-reserve application.
"""

import uvicorn
from backend.app.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "backend.app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if settings.debug else "warning",
    ) 