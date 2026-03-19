from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.bot.handlers.states import AskAIState
from app.bot.keyboards.start_keyboard import reply_keyboard_start
from app.ai.profession import ask_ai_question
from app.db.models import User

ai_router = Router()

AI_QUESTIONS_LIMIT = 5

@ai_router.message(F.text == "Спросить у ИИ")
async def ask_ai_handler(message: Message, state: FSMContext, session: AsyncSession):
    result = await session.execute(
        select(User).where(User.tg_id == message.from_user.id)
    )
    user = result.scalar_one_or_none()

    if not user:
        await message.answer("Произошла ошибка. Попробуйте перезапустить бота командой /start")
        return

    questions_left = AI_QUESTIONS_LIMIT - user.ai_questions_count

    if questions_left <= 0:
        await message.answer(
            f"Вы исчерпали лимит вопросов к ИИ ({AI_QUESTIONS_LIMIT} вопросов).",
            reply_markup=await reply_keyboard_start()
        )
        return

    await state.set_state(AskAIState.waiting_for_question)
    await message.answer(
        f"Задайте свой вопрос искусственному интеллекту.\n"
        f"Осталось вопросов: {questions_left}/{AI_QUESTIONS_LIMIT}",
        reply_markup=await reply_keyboard_start()
    )

@ai_router.message(AskAIState.waiting_for_question)
async def process_ai_question(message: Message, state: FSMContext, session: AsyncSession):
    result = await session.execute(
        select(User).where(User.tg_id == message.from_user.id)
    )
    user = result.scalar_one_or_none()

    if not user:
        await message.answer("Произошла ошибка. Попробуйте перезапустить бота командой /start")
        await state.clear()
        return

    questions_left = AI_QUESTIONS_LIMIT - user.ai_questions_count

    if questions_left <= 0:
        await message.answer(
            f"Вы исчерпали лимит вопросов к ИИ ({AI_QUESTIONS_LIMIT} вопросов).",
            reply_markup=await reply_keyboard_start()
        )
        await state.clear()
        return

    user_question = message.text

    if len(user_question) > 500:
        await message.answer(
            "Вопрос слишком длинный. Пожалуйста, сформулируйте вопрос короче (до 500 символов).",
            reply_markup=await reply_keyboard_start()
        )
        return

    await message.answer("Обрабатываю ваш вопрос...")

    answer = await ask_ai_question(user_question)

    await session.execute(
        update(User)
        .where(User.tg_id == message.from_user.id)
        .values(ai_questions_count=user.ai_questions_count + 1)
    )
    await session.commit()

    questions_left -= 1

    footer = f"\n\nОсталось вопросов: {questions_left}/{AI_QUESTIONS_LIMIT}"
    max_length = 4000

    if len(answer) + len(footer) <= max_length:
        await message.answer(
            f"{answer}{footer}",
            reply_markup=await reply_keyboard_start()
        )
    else:
        chunks = []
        current_chunk = ""
        for paragraph in answer.split('\n'):
            if len(current_chunk) + len(paragraph) + 1 <= max_length:
                current_chunk += paragraph + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = paragraph + '\n'
        if current_chunk:
            chunks.append(current_chunk.strip())

        for i, chunk in enumerate(chunks):
            if i == len(chunks) - 1:
                await message.answer(f"{chunk}{footer}", reply_markup=await reply_keyboard_start())
            else:
                await message.answer(chunk)

    await state.clear()
