from aiogram.types import CallbackQuery
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.profession import response_by_profession_subjects, response_by_info_about_profession

select_profession_router = Router()

@select_profession_router.callback_query(F.data == "subjects_for_pass_exam")
async def info_about_prof(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.answer()
    await callback_query.message.answer(await response_by_profession_subjects(session, callback_query.from_user.id))


@select_profession_router.callback_query(F.data == "info_about_prof")
async def info_about_prof(callback_query: CallbackQuery, session: AsyncSession):
    await callback_query.answer()
    await callback_query.message.answer(await response_by_info_about_profession(session, callback_query.from_user.id))