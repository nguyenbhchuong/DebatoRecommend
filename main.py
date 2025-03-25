from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api
from typing import List
from app.recommendation_service import RecommendationService

app = FastAPI(
    title="Backend API",
    description="RESTful API built with FastAPI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api.router, prefix="/api/v1")

recommendation_service = RecommendationService()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_version": "1.0.0"
    }

@app.post("/recommendations/", response_model=List[str])
async def get_recommendations(tags: List[str]):
    """
    Get related posts based on a list of tags
    """
    if not tags:
        raise HTTPException(status_code=400, detail="Tags list cannot be empty")
    
    try:
        related_posts = recommendation_service.get_related_posts(tags)
        return related_posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 