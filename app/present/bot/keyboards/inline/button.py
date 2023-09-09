from aiogram.types import InlineKeyboardButton

from app.present.bot import locales

from . import callback

send_wallet_address = InlineKeyboardButton(
    text=locales.uk.SEND_WALLET_ADDRESS_BUTTON,
    callback_data=callback.SendWalletAddress().pack(),
)


def previous(page: int) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="⬅️",
        callback_data=callback.Previous(page=page).pack(),
    )


def transaction_index(index: int, next: bool) -> InlineKeyboardButton:
    return InlineKeyboardButton(
        text="➡️" if next else "⬅️",
        callback_data=callback.TransactionIndex(index=index).pack(),
    )


close = InlineKeyboardButton(
    text="❌",
    callback_data=callback.Close().pack(),
)
