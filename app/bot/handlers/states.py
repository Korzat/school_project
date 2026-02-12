from aiogram.fsm.state import StatesGroup, State

class TestPass(StatesGroup):
    answering_question = State()
