from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.profession import response_by_info_about_profession
from app.bot.keyboards.callbacks import ProfessionCallback
from app.bot.keyboards.fisrt_keyboards import select_profession_keyboard
from app.bot.keyboards.professions_keyboards import info_about_profession

professions_router = Router()

@professions_router.message(F.text == "Профессии")
async def select_profession_handler(message: Message):
    await message.answer("Выбери профессию", reply_markup=await select_profession_keyboard())

@professions_router.callback_query(ProfessionCallback.filter())
async def start_handler(callback: CallbackQuery, callback_data: ProfessionCallback, state: FSMContext):
    profession_name = callback_data.profession_name

    await state.update_data(profession=profession_name)

    await callback.message.answer(
        f"Профессия: {profession_name}",
        reply_markup=info_about_profession()
    )
#
# @professions_router.callback_query(F.data == "select_prof_back")
# async def back_to_start_handler(callback: CallbackQuery):
#     await callback.message.edit_text(
#         "Выбери профессию",
#         reply_markup=await select_profession_keyboard()
#     )