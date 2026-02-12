from aiogram.types import CallbackQuery
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from app.ai.profession import response_by_profession_subjects, response_by_info_about_profession

select_profession_router = Router()

@select_profession_router.callback_query(F.data == "subjects_for_pass_exam")
async def info_about_prof(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profession = data.get("profession")
    if not profession:
        await callback_query.message.answer("Сначала выберите профессию с кнопок.")
        return
    text = await response_by_profession_subjects(profession)
    await callback_query.message.answer(text)
    await callback_query.answer()


@select_profession_router.callback_query(F.data == "info_about_prof")
async def info_about_prof(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    profession = data.get("profession")
    if not profession:
        await callback_query.message.answer("Сначала выберите профессию с кнопок.")
        return
    text = await response_by_info_about_profession(profession)
    await callback_query.message.answer(text)
    await callback_query.answer()
