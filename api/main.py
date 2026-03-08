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

init_db()

# -----------------------------------------
# CORS CONFIGURATION
# -----------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    return {
        "platform": "DIMDEA",
        "message": "Carbon Intelligence API Running",
        "status": "online"
    }