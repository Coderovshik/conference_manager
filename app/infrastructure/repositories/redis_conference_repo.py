from typing import List, Optional
from redis import Redis
from domain.entities.conference import Conference
from interfaces.conference_repo import ConferenceRepository

class RedisConferenceRepository(ConferenceRepository):
    KEY_PREFIX = "conference:"

    def __init__(self, redis: Redis):
        self.redis = redis

    def _get_key(self, conference_id: str) -> str:
        return f"{self.KEY_PREFIX}{conference_id}"

    def create_conference(self, conference: Conference) -> Conference:
        if self.get_conference(conference.conference_id):
            raise ValueError(f"Conference with ID {conference.conference_id} already exists")
        self.redis.set(self._get_key(conference.conference_id), conference.model_dump_json())
        return conference

    def get_conference(self, conference_id: str) -> Optional[Conference]:
        data = self.redis.get(self._get_key(conference_id))
        if data:
            return Conference.model_validate_json(data)
        return None

    def update_conference(self, conference_id: str, conference: Conference) -> Conference:
        if not self.get_conference(conference_id):
            raise ValueError(f"Conference with ID {conference_id} not found")
        self.redis.set(self._get_key(conference_id), conference.model_dump_json())
        return conference

    def delete_conference(self, conference_id: str) -> bool:
        if not self.get_conference(conference_id):
            return False
        self.redis.delete(self._get_key(conference_id))
        return True

    def list_conferences(self) -> List[Conference]:
        conferences = []
        for key in self.redis.keys(f"{self.KEY_PREFIX}*"):
            conference = self.get_conference(key.replace(self.KEY_PREFIX, ""))
            if conference:
                conferences.append(conference)
        return conferences