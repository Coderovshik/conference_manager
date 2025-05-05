from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from domain.entities.user import User
from use_cases.user_use_cases import UserUseCases
from infrastructure.repositories.redis_user_repo import RedisUserRepository
from core.redis import get_redis

router = APIRouter(prefix="/auth", tags=["auth"])

class UserCreate(BaseModel):
    username: str
    password: str

def get_use_cases(redis=Depends(get_redis)):
    repo = RedisUserRepository(redis)
    return UserUseCases(repo)

@router.post("/register", response_model=User)
async def register(user_data: UserCreate, use_cases: UserUseCases = Depends(get_use_cases)):
    try:
        user = User(username=user_data.username, password=user_data.password)
        return use_cases.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 