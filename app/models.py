from pydantic import BaseModel, Field, RootModel
from datetime import datetime
from typing import Dict, List, Optional, Any
from bson import ObjectId

class PyObjectId(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler):
        if not isinstance(v, (str, ObjectId)):
            raise TypeError('ObjectId required')
        
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            v = ObjectId(v)
            
        return str(v)

class TopicModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    user_id: PyObjectId
    description: Optional[str] = None
    support_count: int = 0
    oppose_count: int = 0
    file_links: List[str] = Field(default_factory=list)
    tags: Dict[str, float] = Field(default_factory=dict)  # tag name -> weight mapping
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str
        },
        "populate_by_name": True
    }

    def to_dict(self):
        return {
            "_id": str(self.id) if self.id else None,
            "title": self.title,
            "description": self.description,
            "support_count": self.support_count,
            "oppose_count": self.oppose_count,
            "file_links": self.file_links,
            "user_id": str(self.user_id),
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'TopicModel':
        if 'tags' in data and isinstance(data['tags'], list):
            data['tags'] = {tag: 1.0 for tag in data['tags']}
        return cls(**data) 