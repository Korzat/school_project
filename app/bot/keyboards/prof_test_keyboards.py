from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


async def result_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Посмотреть результат",
        callback_data="show_result"
    )
    builder.adjust()
    return builder.as_markup(resize_keyboard=True)

async def yes_no_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Да")
    builder.button(text="Нет")
    builder.adjust()
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
