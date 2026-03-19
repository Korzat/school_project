from aiogram.utils.keyboard import ReplyKeyboardBuilder

async def reply_keyboard_start():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Пройти профориентационный тест")
    builder.button(text="Профессии")
    builder.button(text="Мои увлечения")
    builder.button(text="Спросить у ИИ")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)
    




