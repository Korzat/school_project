from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from app.bot.keyboards.callbacks import ProfessionCallback
from app.db.crud.professions_crud import get_all_professions
from app.db.database import async_session


async def reply_keyboard_skip_the_carrer_guidance_test_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Пропустить профориентационный тест")
    builder.adjust()
    return builder.as_markup(resize_keyboard=True)


async def select_profession_keyboard():
    builder = InlineKeyboardBuilder()
    async with async_session() as session:
        all_professions = await get_all_professions(session)

    for profession in all_professions:
        print(f"DEBUG: ID={profession.id}, Name={getattr(profession, 'profession_name', 'MISSING ATTR')}")

        btn_text = profession.profession_name if profession.profession_name else f"Профессия {profession.id}"

        callback_data = ProfessionCallback(profession_name=profession.profession_name)
        builder.button(
            text=btn_text,
            callback_data=callback_data.pack()
        )

    builder.adjust(1)
    return builder.as_markup()
