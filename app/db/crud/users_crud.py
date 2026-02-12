from sqlalchemy import BigInteger, update, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Profession
from app.db.models.users import User


async def set_user(tg_id: BigInteger, session: AsyncSession) -> None:
    try:
        user = await session.get(User, tg_id)

        if not user:
            new_user = User(tg_id=tg_id, points=0)
            session.add(new_user)
            await session.commit()
            print(f"Пользователь {tg_id} успешно создан.")
        else:
            print(f"Пользователь {tg_id} уже существует.")

    except Exception as e:
        await session.rollback()
        print(f"Ошибка при создании пользователя: {e}")

async def question_yes(tg_id: BigInteger, session: AsyncSession) -> None:
    try:
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(points=User.points + 1)
        )
        await session.commit()

    except Exception:
        await session.rollback()


async def reset_points(tg_id: BigInteger, session: AsyncSession) -> None:
    try:
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(points=0)
        )
        await session.commit()
    except Exception:
        await session.rollback()

async def get_user_points(tg_id: BigInteger, session: AsyncSession) -> int:
    try:
        stmt = select(User.points).where(User.tg_id == tg_id)
        points = await session.scalar(stmt)
        return points if points is not None else 0
    except Exception as e:
        print(f"Ошибка при получении очков пользователя: {e}")
        return 0