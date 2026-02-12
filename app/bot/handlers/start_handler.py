from aiogram.filters import  CommandStart
from aiogram.types import Message
from aiogram import Router
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.keyboards.start_keyboard import reply_keyboard_start
from app.db.crud.users_crud import set_user

start_router = Router()

@start_router.message(CommandStart())
async def start_handler(message: Message, session: AsyncSession):
    await set_user(message.from_user.id, session)
    await message.answer(f"Привет, выбери кнопку!", reply_markup=await reply_keyboard_start())  
