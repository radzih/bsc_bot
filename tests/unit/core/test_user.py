from app.core.user.dto import UserCreate, UserDTO, UserUpdate
from app.core.user.interactor import CreateUser, UpdateUser
from tests.mock.db import DbMockGateway


async def test_create_user(
    create_user: CreateUser, db_gateway: DbMockGateway
) -> None:
    user = UserCreate(name="test", id=1)
    is_created = await create_user(user)

    user_from_db = await db_gateway.get_user(1)

    assert is_created is True
    assert user_from_db is not None
    assert user_from_db.id == user.id
    assert user_from_db.name == user.name
    assert user_from_db.wallet is None


async def test_create_user_error(
    create_user: CreateUser, db_gateway: DbMockGateway
) -> None:
    user1 = UserCreate(name="test1", id=1)
    await create_user(user1)
    user2 = UserCreate(name="test2", id=1)
    is_created = await create_user(user2)

    user_from_db = await db_gateway.get_user(1)

    assert is_created is False
    assert user_from_db is not None
    assert user_from_db.name == user1.name
    assert user_from_db.name != user2.name


async def test_update_user(
    update_user: UpdateUser, db_gateway: DbMockGateway
) -> None:
    await db_gateway.create_user(name="test", id=1)
    await db_gateway.commit()

    user = UserUpdate(id=1, name="test2", wallet="0x123")
    is_updated = await update_user(user)

    user_from_db = await db_gateway.get_user(1)

    assert is_updated is True
    assert user_from_db is not None
    assert user_from_db.id == user.id
    assert user_from_db.name == user.name
    assert user_from_db.wallet == user.wallet
