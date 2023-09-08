from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.present.bot import locales

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        locales.uk.START_MESSAGE.format(name=message.from_user.full_name)
    )
