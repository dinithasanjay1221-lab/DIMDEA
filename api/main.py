# api/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from backend.database_layer import init_db

# -----------------------------------------
# CREATE FASTAPI APP
# -----------------------------------------
app = FastAPI(
    title="DIMDEA API",
    description="Carbon Intelligence Platform",
    version="1.0"
)

# Initialize database safely
try:
    init_db()
except Exception as e:
    print(f"[WARNING] Database initialization failed: {e}")

# -----------------------------------------
# CORS CONFIGURATION
# -----------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------
# INCLUDE ROUTES
# -----------------------------------------
app.include_router(router)

# -----------------------------------------
# ROOT ENDPOINT
# -----------------------------------------
@app.get("/")
def root():
    """
    Root endpoint for health/status check.
    """
    return {
        "platform": "DIMDEA",
        "message": "Carbon Intelligence API Running",
        "status": "online"
    }