from abc import ABC, abstractmethod
from typing import List, Optional
from domain.entities.user import User

class UserRepository(ABC):
    @abstractmethod
    def create_user(self, user: User) -> User:
        """Создает нового пользователя"""
        pass

    @abstractmethod
    def get_user(self, username: str) -> Optional[User]:
        """Получает пользователя по имени пользователя"""
        pass

    @abstractmethod
    def update_user(self, username: str, user: User) -> User:
        """Обновляет данные пользователя"""
        pass

    @abstractmethod
    def delete_user(self, username: str) -> bool:
        """Удаляет пользователя"""
        pass

    @abstractmethod
    def list_users(self) -> List[User]:
        """Возвращает список всех пользователей"""
        pass 