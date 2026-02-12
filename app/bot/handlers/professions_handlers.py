from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.callbacks import ProfessionCallback
from app.bot.keyboards.fisrt_keyboards import select_profession_keyboard
from app.bot.keyboards.professions_keyboards import info_about_profession

professions_router = Router()

@professions_router.message(F.text == "Профессии")
async def select_profession_handler(message: Message):
    await message.answer("Выбери профессию", reply_markup=await select_profession_keyboard())

@professions_router.callback_query(ProfessionCallback.filter())
async def back_to_start_handler(callback: CallbackQuery, callback_data: ProfessionCallback):
    profession_id = callback_data.id

    await callback.message.edit_text(
        f"Информация о профессии №{profession_id}",
        reply_markup=info_about_profession()
    )