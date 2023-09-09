from aiogram.fsm.state import State, StatesGroup


class Wallet(StatesGroup):
    input = State()
