from aiogram import Dispatcher

from . import settings, start, wallet


def include_routers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(wallet.router)
    dp.include_router(settings.router)
