from fastapi import APIRouter, HTTPException
from typing import List
from app.services.recommendation_service import RecommendationService

router = APIRouter()
recommendation_service = RecommendationService()


@router.post("/tags", response_model=List[str])
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
    

@router.post("/posts", response_model=List[str])
async def get_recommendations(postId: str):
    """
    Get related posts based on a post ID
    """
    if not postId:
        raise HTTPException(status_code=400, detail="Post ID cannot be empty")

    try:
        # Check cache first
        cached_results = recommendation_service.get_cached_recommendations(postId)
        if cached_results is not None:
            return cached_results

        # If not in cache, compute recommendations
        post = recommendation_service.get_post(postId)
        if not post.get('tags'): 
            return []
        related_posts = recommendation_service.get_related_posts(post['tags'])
        recommendation_service.cache_by_post_id(postId, related_posts)
        return related_posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# @router.post("/", response_model=List[str])
# async def get_recommendations(tags: List[str]):
#     """
#     Get related posts based on a list of tags
#     """
#     if not tags:
#         raise HTTPException(status_code=400, detail="Tags list cannot be empty")
    
#     try:
#         related_posts = recommendation_service.get_related_posts(tags)
#         return related_posts
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) 