import asyncio
from aiogram import Bot, Dispatcher
from sqlalchemy import insert, select, func

from app.bot.handlers.prof_test_handlers import prof_test_router
from app.bot.handlers.select_profession_handlers import select_profession_router
from app.core.config import settings
from app.db.database import async_session
from app.db.middlewares.database_middleware import DatabaseMiddleware
from app.bot.handlers.start_handler import start_router
from app.bot.handlers.professions_handlers import professions_router
from app.db.models import Profession


async def main():
    data = [
        {"profession_name": "Программист"},
        {"profession_name": "Инженер"},
        {"profession_name": "Экономист"},
        {"profession_name": "Юрист"},
        {"profession_name": "Медик"},
    ]

    async with async_session() as session:
        result = await session.execute(select(func.count()).select_from(Profession))
        count = result.scalar()


    if count == 0:
        async with session.begin():
            await session.execute(insert(Profession), data)
        print(f"База успешно наполнена ({len(data)} профессий)!")
    else:
        print(f"База уже содержит {count} записей. Пропуск наполнения.")
    bot = Bot(token=settings.TOKEN_BOT)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(professions_router)
    dp.include_router(select_profession_router)
    dp.include_router(prof_test_router)

    dp.update.middleware(DatabaseMiddleware(session_pool=async_session))
    await dp.start_polling(bot)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
