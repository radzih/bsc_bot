from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

start = BotCommand(command="start", description="Start bot")
settings = BotCommand(command="settings", description="Settings")
transactions = BotCommand(
    command="transactions", description="Show income transactions"
)

commands = [transactions, settings]


async def set_commands(bot: Bot, user_id: int) -> None:
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())
