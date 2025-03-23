from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from bson import ObjectId

# Add your Pydantic models here 

class Topic:
    def __init__(
        self,
        title: str,
        user_id: ObjectId,
        description: Optional[str] = None,
        support_count: int = 0,
        oppose_count: int = 0,
        file_links: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.title = title
        self.description = description
        self.support_count = support_count
        self.oppose_count = oppose_count
        self.file_links = file_links or []
        self.user_id = user_id
        self.tags = tags or []
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def from_dict(cls, data: dict) -> 'Topic':
        return cls(**data)

    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'description': self.description,
            'support_count': self.support_count,
            'oppose_count': self.oppose_count,
            'file_links': self.file_links,
            'user_id': self.user_id,
            'tags': self.tags,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        } 