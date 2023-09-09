from aiogram import Dispatcher

from . import settings, start, transactions, utils, wallet


def include_routers(dp: Dispatcher):
    dp.include_router(start.router)
    dp.include_router(wallet.router)
    dp.include_router(settings.router)
    dp.include_router(transactions.router)
    dp.include_router(utils.router)
