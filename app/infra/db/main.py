from sqlalchemy import URL, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio.session import async_sessionmaker

from app.core.user.dto import UserDTO

from .config import Database
from .models import User


def create_connection_url(db: Database, async_: bool = False) -> URL:
    return URL.create(
        drivername="postgresql+asyncpg" if async_ else "postgresql",
        username=db.user,
        password=db.password,
        host=db.host,
        port=db.port,
        database=db.name,
    )


def create_session_factory(
    url: URL, echo: bool = False
) -> async_sessionmaker[AsyncSession]:
    engine = create_async_engine(url, echo=echo)
    return async_sessionmaker(bind=engine, class_=AsyncSession)


class DbGateway:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def commit(self) -> None:
        await self._session.commit()

    async def create_user(self, name: str, id: int) -> bool:
        user = User(id=id, name=name)

        self._session.add(user)

        try:
            await self._session.flush()
        except IntegrityError as e:
            await self._session.rollback()
            return False
        return True

    async def update_user(
        self, user_id: int, name: str | None = None, wallet: str | None = None
    ) -> bool:
        user = await self._session.get(User, user_id)
        if not user:
            return False

        if name:
            user.name = name
        if wallet:
            user.wallet = wallet

        self._session.add(user)
        return True

    async def get_user(self, user_id: int) -> UserDTO | None:
        user = await self._session.get(User, user_id)
        if not user:
            return None
        return UserDTO(
            id=user.id,
            name=user.name,
            created_time=user.created_time,
            wallet=user.wallet,
        )

    async def get_users(self) -> list[UserDTO]:
        query = select(User)

        users = await self._session.execute(query)
        return [
            UserDTO(
                id=user.id,
                name=user.name,
                created_time=user.created_time,
                wallet=user.wallet,
            )
            for user in users.scalars()
        ]
