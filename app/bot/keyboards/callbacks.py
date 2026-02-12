from aiogram.filters.callback_data import CallbackData

class ProfessionCallback(CallbackData, prefix="select_profession"):
    id: int