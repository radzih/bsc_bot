from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, User

from app.present.bot import locales
from app.core.user.interactor import CreateUser
from app.core.user import dto

router = Router()


@router.message(CommandStart(), F.from_user.as_("user"))
async def start_handler(message: Message, user: User, create_user: CreateUser) -> None:
    user_create = dto.UserCreate(id=user.id, name=user.full_name)

    await create_user(user_create)

    await message.answer(
        locales.uk.START_MESSAGE.format(name=user.full_name)
    )
