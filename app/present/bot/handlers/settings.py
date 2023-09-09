from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.present.bot import locales
from app.present.bot.keyboards.inline import button
from app.present.bot.services import commands

router = Router()


@router.message(Command(commands.settings))
async def settings(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(button.send_wallet_address)

    await message.answer(
        text=locales.uk.SETTINGS_MESSAGE,
        reply_markup=builder.as_markup(),
    )
