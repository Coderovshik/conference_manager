import json
from typing import List, Optional
from redis import Redis
from domain.entities.conference import Conference
from interfaces.conference_repo import ConferenceRepository

class RedisConferenceRepository(ConferenceRepository):
    def __init__(self, redis: Redis):
        self.redis = redis

    def create_conference(self, conference: Conference) -> Conference:
        if self.get_conference(conference.id):
            raise ValueError(f"Конференция с ID {conference.id} уже существует")
        self.redis.set(conference.id, conference.json())
        return conference

    def get_conference(self, conference_id: str) -> Optional[Conference]:
        data = self.redis.get(conference_id)
        if data:
            return Conference(**json.loads(data))
        return None

    def update_conference(self, conference_id: str, conference: Conference) -> Conference:
        if not self.get_conference(conference_id):
            raise ValueError(f"Конференция с ID {conference_id} не найдена")
        self.redis.set(conference_id, conference.json())
        return conference

    def delete_conference(self, conference_id: str) -> bool:
        if not self.get_conference(conference_id):
            return False
        self.redis.delete(conference_id)
        return True

    def list_conferences(self) -> List[Conference]:
        conferences = []
        for key in self.redis.keys():
            conference = self.get_conference(key)
            if conference:
                conferences.append(conference)
        return conferences