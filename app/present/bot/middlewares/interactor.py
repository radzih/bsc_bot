from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.config import Config
from app.core.transaction.interactor import ListTransactions
from app.core.user.interactor import CreateUser, UpdateUser
from app.core.wallet.interactor import IsValidWallet
from app.infra.bscscan.main import BSCScanAdapter
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
        config: Config = data["config"]
        db = DbGateway(db_session)
        bscscan = BSCScanAdapter(config.bscscan.api_key)

        data["create_user"] = CreateUser(db)
        data["update_user"] = UpdateUser(db)
        data["is_valid_wallet"] = IsValidWallet(bscscan)
        data["list_transactions"] = ListTransactions(db, bscscan)

        await handler(event, data)
        await db_session.close()
        await bscscan.session.close()
