from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.core.user.interactor import CreateUser
from app.infra.db.main import DbGateway


class InteractorMiddleware(BaseMiddleware):
    def __init__(
        self,
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> None:
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[
            [TelegramObject, Dict[str, Any]],
            Awaitable[Any],
        ],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        db_session = self.sessionmaker()
        db = DbGateway(db_session)

        data["create_user"] = CreateUser(db)

        await handler(event, data)
        await db_session.close()
