from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.handlers.states import HobbiesState
from app.bot.keyboards.start_keyboard import reply_keyboard_start
from app.utils.hobbies_analyzer import analyze_hobbies
from app.bot.keyboards.professions_keyboards import info_about_profession

hobbies_router = Router()

@hobbies_router.message(F.text == "Мои увлечения")
async def hobbies_handler(message: Message, state: FSMContext):
    await state.set_state(HobbiesState.waiting_for_hobbies)
    await message.answer(
        "Расскажите о своих увлечениях и интересах. Опишите, чем вы любите заниматься в свободное время:",
        reply_markup=await reply_keyboard_start()
    )

@hobbies_router.message(HobbiesState.waiting_for_hobbies)
async def process_hobbies(message: Message, state: FSMContext):
    user_text = message.text

    profession = analyze_hobbies(user_text)

    if profession:
        await state.update_data(profession=profession)
        await message.answer(
            f"На основе ваших увлечений вам может подойти профессия: {profession}\n\n"
            f"Хотите узнать больше об этой профессии?",
            reply_markup=info_about_profession()
        )
    else:
        await message.answer(
            "К сожалению, не удалось определить подходящую профессию на основе ваших увлечений. "
            "Попробуйте описать свои интересы более подробно или выберите профессию из списка.",
            reply_markup=await reply_keyboard_start()
        )

    await state.clear()
