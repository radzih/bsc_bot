from aiogram.types import InlineKeyboardButton

from app.present.bot import locales

from . import callback

send_wallet_address = InlineKeyboardButton(
    text=locales.uk.SEND_WALLET_ADDRESS_BUTTON,
    callback_data=callback.SendWalletAddress().pack(),
)


close = InlineKeyboardButton(
    text="❌",
    callback_data=callback.Close().pack(),
)
