from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "password123"
            }
        } 