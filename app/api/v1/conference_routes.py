from fastapi import APIRouter, Depends, HTTPException
from typing import List
from domain.entities.conference import Conference
from domain.entities.user import User
from use_cases.conference_use_cases import ConferenceUseCases
from infrastructure.repositories.redis_conference_repo import RedisConferenceRepository
from core.redis import get_redis
from core.auth import get_current_user

router = APIRouter(prefix="/conferences", tags=["conferences"])

def get_use_cases(redis=Depends(get_redis)):
    repo = RedisConferenceRepository(redis)
    return ConferenceUseCases(repo)

@router.post("/", response_model=Conference)
async def create_conference(
    conference: Conference,
    use_cases: ConferenceUseCases = Depends(get_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        return use_cases.create_conference(conference)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{conference_id}", response_model=Conference)
async def get_conference(
    conference_id: str,
    use_cases: ConferenceUseCases = Depends(get_use_cases),
    current_user: User = Depends(get_current_user)
):
    conference = use_cases.get_conference(conference_id)
    if not conference:
        raise HTTPException(status_code=404, detail="Конференция не найдена")
    return conference

@router.put("/{conference_id}", response_model=Conference)
async def update_conference(
    conference_id: str,
    conference: Conference,
    use_cases: ConferenceUseCases = Depends(get_use_cases),
    current_user: User = Depends(get_current_user)
):
    try:
        return use_cases.update_conference(conference_id, conference)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{conference_id}")
async def delete_conference(
    conference_id: str,
    use_cases: ConferenceUseCases = Depends(get_use_cases),
    current_user: User = Depends(get_current_user)
):
    if not use_cases.delete_conference(conference_id):
        raise HTTPException(status_code=404, detail="Конференция не найдена")
    return {"message": "Конференция успешно удалена"}

@router.get("/", response_model=List[Conference])
async def list_conferences(
    use_cases: ConferenceUseCases = Depends(get_use_cases),
    current_user: User = Depends(get_current_user)
):
    return use_cases.list_conferences()