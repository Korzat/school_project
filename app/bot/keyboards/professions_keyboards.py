

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import  InlineKeyboardBuilder


def info_about_profession() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Узнать больше о профессии", callback_data="info_about_prof")
    builder.button(text="Нужные предметы для сдачи ЕГЭ", callback_data="subjects_for_pass_exam")
    builder.button(text="<- Назад", callback_data="select_prof_back")

    builder.adjust(1, 1)

    return builder.as_markup(resize_keyboard=True)




