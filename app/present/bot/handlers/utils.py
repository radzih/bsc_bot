from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from app.present.bot.keyboards.inline import callback

router = Router()


@router.callback_query(callback.Close.filter())
async def close(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.delete()
