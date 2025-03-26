from typing import List
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from pymongo import MongoClient
import redis
import json
import config
from fastapi import HTTPException
from bson import ObjectId

class RecommendationService:
    def __init__(self):
        # Initialize MongoDB connection
        self.mongo_client = MongoClient(config.MONGODB_URI)
        self.db = self.mongo_client[config.MONGODB_DB]
        self.posts_collection = self.db['topics']
        
        # Initialize Redis connection
        self.redis_client = redis.Redis(
            host=config.REDIS_HOST,
            port=config.REDIS_PORT,
            db=config.REDIS_DB,
            decode_responses=True
        )

    def get_post(self, post_id: str):
        """
        Retrieve a post by its ID
        
        Args:
            post_id (str): The ID of the post to retrieve
            
        Returns:
            Post: The post object
            
        Raises:
            HTTPException: If the post is not found
        """
        topic_id = ObjectId(post_id)
        post = self.posts_collection.find_one({"_id": topic_id})
        if not post:
            raise HTTPException(status_code=404, detail=f"Post with id {post_id} not found")
        return post

    def get_related_posts(self, tags: List[str], max_posts: int = 10) -> List[str]:
        """
        Find related posts based on tag similarity using cosine similarity
        
        Args:
            tags: List of tags to find related posts for
            max_posts: Maximum number of posts to return (default: 10)
            
        Returns:
            List of post IDs of related posts
        """

        # Get all posts with their tags from MongoDB
        all_posts = list(self.posts_collection.find({'tags': {'$exists': True}}, {'_id': 1, 'tags': 1}))
        if not all_posts:
            return []
       
        # Create a set of all unique tags
        all_unique_tags = set()
        for post in all_posts:
            all_unique_tags.update(post.get('tags', []))
        
        # Convert tags to vector space
        tag_to_index = {tag: i for i, tag in enumerate(all_unique_tags)}
        
        # Create vector for input tags
        input_vector = np.zeros(len(tag_to_index))
        for tag in tags:
            if tag in tag_to_index:
                input_vector[tag_to_index[tag]] = 1

        # Create vectors for all posts
        post_vectors = []
        post_ids = []
        for post in all_posts:
            vector = np.zeros(len(tag_to_index))
            for tag in post.get('tags', []):
                vector[tag_to_index[tag]] = 1
            post_vectors.append(vector)
            post_ids.append(str(post['_id']))

        # Convert to numpy array
        post_vectors = np.array(post_vectors)
        
        # Calculate cosine similarity
        similarities = cosine_similarity([input_vector], post_vectors)[0]
        
        # Get indices of top similar posts
        similar_indices = np.argsort(similarities)[::-1][:max_posts]
        
        # Return post IDs of most similar posts
        return [post_ids[i] for i in similar_indices if similarities[i] > 0] 
    
    def cache_by_post_id(self, post_id: str, related_posts: List[str]):
        """
        Cache the related posts for a post ID
        """
        self.redis_client.set(f"related_posts:{post_id}", json.dumps(related_posts))
        self.redis_client.expire(f"related_posts:{post_id}", 300)  # 5 minutes

    def get_cached_recommendations(self, post_id: str) -> List[str]:
        """
        Get cached recommendations for a post ID
        
        Args:
            post_id (str): The ID of the post
            
        Returns:
            List[str]: List of related post IDs or None if not cached
        """
        cached = self.redis_client.get(f"related_posts:{post_id}")
        if cached:
            return json.loads(cached)
        return None

