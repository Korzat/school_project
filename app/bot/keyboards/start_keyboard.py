from aiogram.utils.keyboard import ReplyKeyboardBuilder, ReplyKeyboardMarkup

async def reply_keyboard_start():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Пройти профориентационный тест")
    builder.button(text="Профессии")
    # builder.button(text="Помощь")
    builder.adjust()
    return builder.as_markup(resize_keyboard=True)
    




