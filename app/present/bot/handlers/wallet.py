from aiogram import Bot, F, Router
from aiogram.filters.state import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, User

from app.core.user import dto
from app.core.user.interactor import UpdateUser
from app.present.bot import locales
from app.present.bot.filters.wallet import WalletFilter
from app.present.bot.keyboards.inline import callback
from app.present.bot.services import states

router = Router()


@router.callback_query(
    callback.SendWalletAddress.filter(), F.message.as_("message")
)
async def input_wallet_address(
    call: CallbackQuery, state: FSMContext, message: Message
) -> None:
    await call.answer()

    sended = await message.edit_text(text=locales.uk.WALLET_INPUT_MESSAGE)

    await state.set_state(states.Wallet.input)
    await state.update_data(last_message_id=sended.message_id)


@router.message(
    StateFilter(states.Wallet.input),
    F.from_user.as_("user"),
    WalletFilter(valid=True),
)
async def save_wallet(
    message: Message,
    state: FSMContext,
    update_user: UpdateUser,
    user: User,
    bot: Bot,
) -> None:
    state_data = await state.get_data()
    await state.clear()

    wallet_address = message.text

    await update_user(
        dto.UserUpdate(
            id=user.id,
            wallet=wallet_address,
        )
    )

    await bot.delete_message(user.id, state_data["last_message_id"])

    await message.answer(text=locales.uk.WALLET_INPUT_SUCCESS_MESSAGE)


@router.message(
    StateFilter(states.Wallet.input),
    F.from_user.as_("user"),
    WalletFilter(valid=False),
)
async def invalid_wallet(
    message: Message,
    state: FSMContext,
    user: User,
    bot: Bot,
) -> None:
    state_data = await state.get_data()

    await message.delete()
    await bot.delete_message(user.id, state_data["last_message_id"])

    sended = await message.answer(text=locales.uk.WALLET_INPUT_ERROR_MESSAGE)

    await state.update_data(last_message_id=sended.message_id)
