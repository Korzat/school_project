from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.models.professions import Profession


async def create_profession(profession_name: str, session: AsyncSession) -> None:
    try:
        new_profession = Profession(profession_name=profession_name)
        session.add(new_profession)
        await session.commit()
        print(f"Профессия {profession_name} успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании профессии: {e}")

async def delete_profession(profession_id: int, session: AsyncSession) -> None:
    try:
        profession = await session.execute(select(Profession).where(Profession.id == profession_id))
        profession = profession.scalar_one_or_none()
        if profession:
            await session.delete(profession)
            await session.commit()
            print(f"Профессия {profession_id} успешно удалена.")
        else:
            print(f"Профессия {profession_id} не найдена.")
    except Exception as e:
        await session.rollback()
        print(f"Ошибка при удалении профессии: {e}")

async def get_all_professions(session: AsyncSession) -> list:
    try:
        result = await session.execute(select(Profession))
        return result.scalars().all()
    except Exception as e:
        print(f"Ошибка при получении профессий: {e}")
        return []

async def get_profession_name(session: AsyncSession, tg_id: int):
    try:
        stmt = (
            select(Profession.profession_name)
            .join(User, User.profession == Profession.id)
            .where(User.tg_id == tg_id)
        )

        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    except Exception as e:
        print("DB error:", e)
        return None



