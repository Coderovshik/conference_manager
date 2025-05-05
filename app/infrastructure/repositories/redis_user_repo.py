from typing import List, Optional
from redis import Redis
from domain.entities.user import User
from interfaces.user_repo import UserRepository

class RedisUserRepository(UserRepository):
    KEY_PREFIX = "user:"

    def __init__(self, redis: Redis):
        self.redis = redis

    def _get_key(self, username: str) -> str:
        return f"{self.KEY_PREFIX}{username}"

    def create_user(self, user: User) -> User:
        if self.get_user_by_username(user.username):
            raise ValueError(f"Пользователь с именем {user.username} уже существует")
        self.redis.set(self._get_key(user.username), user.model_dump_json())
        return user

    def get_user(self, username: str) -> Optional[User]:
        data = self.redis.get(self._get_key(username))
        if data:
            return User.model_validate_json(data)
        return None

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.get_user(username)

    def update_user(self, username: str, user: User) -> User:
        if not self.get_user(username):
            raise ValueError(f"Пользователь с именем {username} не найден")
        self.redis.set(self._get_key(username), user.model_dump_json())
        return user

    def delete_user(self, username: str) -> bool:
        if not self.get_user(username):
            return False
        self.redis.delete(self._get_key(username))
        return True

    def list_users(self) -> List[User]:
        users = []
        for key in self.redis.keys(f"{self.KEY_PREFIX}*"):
            user = self.get_user(key.decode().replace(self.KEY_PREFIX, ""))
            if user:
                users.append(user)
        return users 