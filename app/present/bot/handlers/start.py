from aiogram import Bot, F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, User
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.user import dto
from app.core.user.interactor import CreateUser
from app.present.bot import locales
from app.present.bot.keyboards.inline import button
from app.present.bot.services import commands

router = Router()


@router.message(CommandStart(), F.from_user.as_("user"))
async def start_handler(
    message: Message, user: User, create_user: CreateUser, bot: Bot
) -> None:
    user_create = dto.UserCreate(id=user.id, name=user.full_name)

    await create_user(user_create)

    builder = InlineKeyboardBuilder()
    builder.add(button.send_wallet_address)

    await commands.set_commands(bot, user.id)

    await message.answer(
        locales.uk.START_MESSAGE.format(name=user.full_name),
        reply_markup=builder.as_markup(),
    )
