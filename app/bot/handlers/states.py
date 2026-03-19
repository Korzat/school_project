from aiogram.fsm.state import StatesGroup, State

class TestPass(StatesGroup):
    answering_question = State()

class HobbiesState(StatesGroup):
    waiting_for_hobbies = State()

class AskAIState(StatesGroup):
    waiting_for_question = State()
