from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

# Utility for ObjectId validation/serialization
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ChatEntry(BaseModel):
    user_id: str = Field(..., description="User's MongoDB ObjectId as string")
    question: str
    answer: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        json_encoders = {ObjectId: str}

class Chat(BaseModel):
    user_id: str
    question: str
