import asyncio
from aiogram import Bot, Dispatcher
from sqlalchemy import insert, select, func

from app.bot.handlers.prof_test_handlers import prof_test_router
from app.bot.handlers.select_profession_handlers import select_profession_router
from app.bot.handlers.hobbies_handlers import hobbies_router
from app.bot.handlers.ai_handlers import ai_router
from app.core.config import settings
from app.db.database import async_session
from app.db.middlewares.database_middleware import DatabaseMiddleware
from app.bot.handlers.start_handler import start_router
from app.bot.handlers.professions_handlers import professions_router
from app.db.models import Profession


async def main():
    from app.db.models import University, ProfessionsUniversities

    professions_data = [
        {"profession_name": "Программист"},
        {"profession_name": "Инженер"},
        {"profession_name": "Врач"},
        {"profession_name": "Юрист"},
        {"profession_name": "Экономист"},
    ]

    universities_data = [
        {"university_name": "МГУ имени М.В. Ломоносова", "description": "Ведущий классический университет России"},
        {"university_name": "МГТУ имени Н.Э. Баумана", "description": "Технический университет"},
        {"university_name": "НИУ ВШЭ", "description": "Национальный исследовательский университет"},
        {"university_name": "МФТИ", "description": "Московский физико-технический институт"},
        {"university_name": "Первый МГМУ имени И.М. Сеченова", "description": "Медицинский университет"},
        {"university_name": "РНИМУ имени Н.И. Пирогова", "description": "Медицинский университет"},
        {"university_name": "МГЮА имени О.Е. Кутафина", "description": "Юридическая академия"},
        {"university_name": "МГИМО", "description": "Международный институт"},
        {"university_name": "РЭУ имени Г.В. Плеханова", "description": "Экономический университет"},
        {"university_name": "Финансовый университет", "description": "Финансовый университет при Правительстве РФ"},
    ]

    profession_university_links = [
        (1, 1), (1, 2),
        (2, 2), (2, 4),
        (3, 5), (3, 6),
        (4, 7), (4, 8),
        (5, 9), (5, 10),
    ]

    async with async_session() as session:
        result = await session.execute(select(func.count()).select_from(Profession))
        count = result.scalar()

        if count == 0:
            await session.execute(insert(Profession), professions_data)
            await session.execute(insert(University), universities_data)

            for prof_id, univ_id in profession_university_links:
                await session.execute(
                    insert(ProfessionsUniversities).values(
                        profession_id=prof_id,
                        university_id=univ_id
                    )
                )
        await session.commit()
        print(f"База успешно наполнена ({len(professions_data)} профессий, {len(universities_data)} университетов)!")

    bot = Bot(token=settings.TOKEN_BOT)
    dp = Dispatcher()
    dp.include_router(start_router)
    dp.include_router(professions_router)
    dp.include_router(select_profession_router)
    dp.include_router(prof_test_router)
    dp.include_router(hobbies_router)
    dp.include_router(ai_router)

    dp.update.middleware(DatabaseMiddleware(session_pool=async_session))
    await dp.start_polling(bot)



if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Ошибка при запуске бота: {e}")
