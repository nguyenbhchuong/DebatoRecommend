from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api

def create_application() -> FastAPI:
    application = FastAPI(
        title="Backend API",
        description="RESTful API built with FastAPI",
        version="1.0.0"
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    application.include_router(api.router, prefix="/api/v1")

    return application

app = create_application() 