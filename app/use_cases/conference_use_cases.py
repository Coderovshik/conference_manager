from typing import List, Optional
from domain.entities.conference import Conference
from interfaces.conference_repo import ConferenceRepository

class ConferenceUseCases:
    def __init__(self, conference_repository: ConferenceRepository):
        self.conference_repository = conference_repository

    def create_conference(self, conference: Conference) -> Conference:
        return self.conference_repository.create_conference(conference)

    def get_conference(self, conference_id: str) -> Optional[Conference]:
        return self.conference_repository.get_conference(conference_id)

    def update_conference(self, conference_id: str, conference: Conference) -> Conference:
        return self.conference_repository.update_conference(conference_id, conference)

    def delete_conference(self, conference_id: str) -> bool:
        return self.conference_repository.delete_conference(conference_id)

    def list_conferences(self) -> List[Conference]:
        return self.conference_repository.list_conferences()