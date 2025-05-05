from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.conference import Conference

class ConferenceRepository(ABC):
    @abstractmethod
    def create_conference(self, conference: Conference) -> Conference:
        pass

    @abstractmethod
    def get_conference(self, conference_id: str) -> Optional[Conference]:
        pass

    @abstractmethod
    def update_conference(self, conference_id: str, conference: Conference) -> Conference:
        pass

    @abstractmethod
    def delete_conference(self, conference_id: str) -> bool:
        pass

    @abstractmethod
    def list_conferences(self) -> List[Conference]:
        pass