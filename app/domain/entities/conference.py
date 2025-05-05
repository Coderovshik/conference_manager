from pydantic import BaseModel, HttpUrl, EmailStr
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ConferenceStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class Conference(BaseModel):
    id: str
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    status: ConferenceStatus = ConferenceStatus.DRAFT
    
    # Meeting link
    meeting_link: Optional[HttpUrl]
    
    # Additional fields
    organizer_email: EmailStr
    max_participants: Optional[int]
    registration_deadline: Optional[datetime]
    timezone: str = "UTC"
    tags: List[str] = []
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "conf-001",
                "title": "Python Web Development Workshop",
                "description": "Learn about modern Python web development",
                "start_time": "2024-03-20T10:00:00Z",
                "end_time": "2024-03-20T18:00:00Z",
                "status": "scheduled",
                "meeting_link": "https://zoom.us/j/123456789",
                "organizer_email": "organizer@example.com",
                "max_participants": 100,
                "registration_deadline": "2024-03-19T23:59:59Z",
                "timezone": "UTC",
                "tags": ["python", "web", "workshop"]
            }
        }