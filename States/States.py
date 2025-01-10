from aiogram.fsm.state import StatesGroup, State


class LinkAnswer(StatesGroup):
    getAnswer = State()
