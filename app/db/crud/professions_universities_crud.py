from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ProfessionsUniversities


async def create_professions_universities(profession_id: int, university_id: int, session: AsyncSession) -> None:
    try:
        session.add(ProfessionsUniversities(profession_id=profession_id, university_id=university_id))
        await session.commit()
        print(f"Связь между профессией {profession_id} и университетом {university_id} успешно создана.")
    except Exception as e:
        await session.rollback()
        print(f"Ошибка при создании связи между профессией и университетом: {e}")

