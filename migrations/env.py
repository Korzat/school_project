import os
import sys
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine

from app.core.config import settings
from app.db.models import professions, professions_universities, universities, users
from app.db.base_model import Base
from alembic import context

# --- Настройка путей ---
# Определяем корневую директорию проекта (на уровень выше папки alembic)
current_path = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_path, '..'))
# Добавляем в путь, чтобы Python видел пакет 'app'
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Импорт моделей ---
# Импортируем Base ПОСЛЕ настройки путей

# --- Конфигурация Alembic ---
config = context.config

# Настройка логирования
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для автогенерации
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Запуск миграций в 'offline' режиме."""
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """
    Синхронная функция-обертка.
    Именно она вызывается внутри run_sync и получает синхронное соединение.
    """
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Запуск миграций в 'online' режиме."""

    # Получаем URL из alembic.ini или переменной окружения
    # Убедитесь, что в URL используется драйвер asyncpg (postgresql+asyncpg://...)
    url = settings.DATABASE_URL

    connectable = create_async_engine(
        url,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        # Важно: передаем функцию do_run_migrations в run_sync.
        # SQLAlchemy создаст синхронную сессию и передаст её аргументом в функцию.
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    # Используем asyncio.run для запуска асинхронной функции
    asyncio.run(run_migrations_online())