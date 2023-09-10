from math import ceil

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.filters.exception import ExceptionTypeFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ErrorEvent, Message, User
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.transaction.dto import TransactionDTO, TransactionsList
from app.core.transaction.exception import WalletNotSet
from app.core.transaction.interactor import ListTransactions
from app.present.bot import locales
from app.present.bot.keyboards.inline import button, callback
from app.present.bot.services import commands

router = Router()

PER_PAGE = 500
FIRST_INDEX = 0
FIRST_PAGE = 0


@router.message(F.from_user.as_("user"), Command(commands.transactions))
async def show_transactions(
    message: Message,
    list_transactions: ListTransactions,
    user: User,
    state: FSMContext,
) -> None:
    transactions = await list_transactions(
        TransactionsList(user_id=user.id, page=FIRST_PAGE, per_page=PER_PAGE)
    )
    transaction = transactions[FIRST_INDEX]
    await state.update_data(transactions=transactions)

    keyboard = transaction_keyboard(FIRST_INDEX, len(transactions) - 1)
    text = transaction_text(transaction)

    await message.answer(
        text=text,
        reply_markup=keyboard,
    )


@router.callback_query(
    F.from_user.as_("user"),
    callback.TransactionIndex.filter(),
    F.message.as_("message"),
)
async def show_transaction_call(
    call: CallbackQuery,
    list_transactions: ListTransactions,
    message: Message,
    user: User,
    callback_data: callback.TransactionIndex,
    state: FSMContext,
) -> None:
    await call.answer()

    state_data = await state.get_data()

    if not state_data.get("transactions"):
        await message.delete()
        return await show_transactions(
            message=message,
            list_transactions=list_transactions,
            user=user,
            state=state,
        )
    transactions: list[TransactionDTO] = state_data["transactions"]

    if callback_data.index == len(transactions) - 1:
        transactions = await update_transactions_in_state(
            list_transactions=list_transactions,
            old_transactions=transactions,
            user=user,
            state=state,
            offset=PER_PAGE,
            page=ceil(callback_data.index + 1 / PER_PAGE),
        )

    transaction = transactions[callback_data.index]
    text = transaction_text(transaction)
    keyboard = transaction_keyboard(callback_data.index, len(transactions) - 1)

    await message.edit_text(
        text=text,
        reply_markup=keyboard,
    )


@router.error(
    ExceptionTypeFilter(WalletNotSet), F.update.message.as_("message")
)
async def wallet_not_set_error(
    event: ErrorEvent,
    message: Message,
) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(button.send_wallet_address)

    await message.answer(
        text=locales.uk.WALLET_NOT_SET_MESSAGE,
        reply_markup=builder.as_markup(),
    )


async def update_transactions_in_state(
    list_transactions: ListTransactions,
    old_transactions: list[TransactionDTO],
    user: User,
    state: FSMContext,
    page: int,
) -> list[TransactionDTO]:
    transactions = await list_transactions(
        TransactionsList(user_id=user.id, page=page, per_page=PER_PAGE)
    )
    await state.update_data(transactions=old_transactions + transactions)
    state_data = await state.get_data()
    transactions = state_data["transactions"]
    return transactions


def transaction_keyboard(
    index: int, total_items: int
) -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.adjust(1, repeat=True)

    navigation = []
    if index > FIRST_INDEX:
        navigation.append(
            button.transaction_index(index=index - 1, next=False)
        )
    if index < total_items:
        navigation.append(button.transaction_index(index=index + 1, next=True))

    builder.row(*navigation)
    builder.row(button.close)

    return builder.as_markup()


def transaction_text(transaction: TransactionDTO) -> str:
    return locales.uk.TRANSACTION_MESSAGE.format(
        hash=transaction.hash,
        block=1,
        from_address=1,
        to_address=2,
        amount_in_bnb=transaction.amount_in_bnb,
        amount_in_usd=transaction.amount_in_usd_now,
        type=locales.uk.TYPE_TO_UK[transaction.type.value],
        date=transaction.time.strftime("%d.%m.%Y %H:%M:%S"),
        status=locales.uk.STATUS_TO_UK[transaction.status.value],
    )
