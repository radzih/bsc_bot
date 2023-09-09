from aiogram.filters.callback_data import CallbackData


class SendWalletAddress(CallbackData, prefix="send_wallet_address"):
    pass


class Close(CallbackData, prefix="close"):
    pass

