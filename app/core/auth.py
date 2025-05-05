from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from use_cases.user_use_cases import UserUseCases
from infrastructure.repositories.redis_user_repo import RedisUserRepository
from core.redis import get_redis

security = HTTPBasic()

def get_auth_use_cases(redis=Depends(get_redis)):
    repo = RedisUserRepository(redis)
    return UserUseCases(repo)

def get_current_user(
    credentials: HTTPBasicCredentials = Security(security),
    use_cases: UserUseCases = Depends(get_auth_use_cases)
):
    user = use_cases.get_user(credentials.username)
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=401,
            detail="Неверные учетные данные",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user