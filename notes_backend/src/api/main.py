from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.notes import router as notes_router
from src.db.session import init_db

openapi_tags = [
    {"name": "Health", "description": "Service health and status endpoints."},
    {"name": "Notes", "description": "Operations for creating, reading, updating, and deleting notes."},
]

app = FastAPI(
    title="Notes Backend API",
    description="API for managing personal notes with CRUD operations.",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Initialize database on startup."""
    init_db()


# PUBLIC_INTERFACE
@app.get(
    "/",
    tags=["Health"],
    summary="Health Check",
    description="Simple health check endpoint to verify the service is running.",
    responses={200: {"description": "Service healthy."}},
)
def health_check():
    """Returns simple health status."""
    return {"message": "Healthy"}


# Register routers
app.include_router(notes_router)
