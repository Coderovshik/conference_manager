from typing import List, Optional
from domain.entities.user import User
from interfaces.user_repo import UserRepository

class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, user: User) -> User:
        return self.user_repository.create_user(user)

    def get_user(self, username: str) -> Optional[User]:
        return self.user_repository.get_user(username)

    def update_user(self, username: str, user: User) -> User:
        return self.user_repository.update_user(username, user)

    def delete_user(self, username: str) -> bool:
        return self.user_repository.delete_user(username)

    def list_users(self) -> List[User]:
        return self.user_repository.list_users() 