from typing import Any

from aiogram.filters import Command, Filter
from aiogram.types import Message

from app.core.wallet.interactor import IsValidWallet


class WalletFilter(Filter):
    def __init__(self, valid: bool):
        self.valid = valid

    async def __call__(
        self, message: Message, is_valid_wallet: IsValidWallet
    ) -> bool | dict:
        wallet = message.text
        is_valid = await is_valid_wallet(wallet)

        if is_valid and self.valid:
            return {"wallet": wallet}
        return is_valid is self.valid
