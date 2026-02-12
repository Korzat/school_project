from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.universities import University


async def create_university(university_name: str, description: str, session: AsyncSession) -> None:
    try:
        new_university = University(university_name=university_name, description=description)
        session.add(new_university)
        await session.commit()
        print(f"Университет {university_name} успешно создан.")
    except Exception as e:
        print(f"Ошибка при создании университета: {e}")

