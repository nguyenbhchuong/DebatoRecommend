from fastapi import APIRouter
from app.routes import recommendations

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "api_version": "1.0.0"
    }

router.include_router(
    recommendations.router,
    prefix="/recommendations",
    tags=["recommendations"]
)

@router.get("/example")
async def example_route():
    return {"message": "This is an example route"} 