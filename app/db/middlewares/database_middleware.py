from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        # Создаем новую сессию для каждого запроса (update)
        async with self.session_pool() as session:
            # Добавляем объект сессии в 'data',
            # чтобы он стал доступен в аргументах хендлера (start_handler)
            data["session"] = session
            # Передаем управление дальше по цепочке middlewares к вашему хендлеру
            return await handler(event, data)

