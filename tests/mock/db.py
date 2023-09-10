from datetime import datetime

from app.core.user.dto import UserDTO
from app.infra.db.main import DbGateway


class DbMockGateway(DbGateway):
    def __init__(self) -> None:
        self.users = {}
        self.users_to_commit = []

    async def commit(self) -> None:
        for user in self.users_to_commit:
            self.users[user.id] = user
        self.users_to_commit = []

    async def create_user(self, name: str, id: int) -> bool:
        if id in self.users:
            return False
        user = UserDTO(id=id, name=name, created_time=datetime.now())
        self.users_to_commit.append(user)
        return True

    async def update_user(
        self, user_id: int, name: str | None = None, wallet: str | None = None
    ) -> bool:
        if user_id not in self.users:
            return False

        user = self.users[user_id]
        if name:
            user.name = name
        if wallet:
            user.wallet = wallet

        self.users_to_commit.append(user)
        return True

    async def get_user(self, user_id: int) -> UserDTO | None:
        if user_id not in self.users:
            return None
        return self.users[user_id]

    async def get_users(self) -> list[UserDTO]:
        return list(self.users.values())
