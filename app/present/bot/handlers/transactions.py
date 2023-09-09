from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message, User

from app.present.bot.services import commands

router = Router()


@router.message(Command(commands.transactions), F.from_user.as_("user"))
async def show_transactions(message: Message, user: User):
    pass
