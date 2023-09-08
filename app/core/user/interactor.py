from app.core.shared.interactor import Interactor
from app.infra.db.main import DbGateway

from . import dto


class CreateUser(Interactor):
    def __init__(self, db: DbGateway) -> None:
        self.db = db

    async def __call__(self, data: dto.UserCreate) -> bool:
        """
        Create user in database.
        Return True if user was created, False if user already exists.
        """
        is_created = await self.db.create_user(name=data.name, id=data.id)
        await self.db.commit()
        return is_created


class UpdateUser(Interactor):
    def __init__(self, db: DbGateway) -> None:
        self.db = db

    async def __call__(self, data: dto.UserUpdate) -> bool:
        """
        Update user in database.
        Return True if user was updated, False if user does not exist.
        """
        is_updated = await self.db.update_user(
            user_id=data.id, name=data.name, wallet=data.wallet
        )
        await self.db.commit()

        return is_updated
