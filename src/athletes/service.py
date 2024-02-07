from typing import Type

from fastapi import HTTPException, status
from sqlalchemy import Result, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.athletes.models import Athlete
from src.athletes.schemas import AthleteCreate
from src.exceptions import ResponseError


async def get_athletes(session: AsyncSession) -> list[Athlete]:
    """Получение данных всех спортсменов"""

    try:
        query = select(Athlete).order_by(Athlete.id)
        result: Result = await session.execute(query)
        athletes: list[Athlete] = list(result.scalars().all())
        return athletes
    except Exception as e:
        raise ResponseError(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f" Ошибка: {e}", e=e
        )


async def create_athlete(athlete: AthleteCreate, session: AsyncSession) -> Athlete:
    """Добавление данных спортсмена в БД"""

    # Проверяем, существует ли уже спортсмен с такими же данными
    existing_athlete = await session.execute(
        select(Athlete).where(
            (Athlete.first_name == athlete.first_name)
            & (Athlete.last_name == athlete.last_name)
            & (Athlete.age == athlete.age)
            & (Athlete.country == athlete.country)
            & (Athlete.sport_id == athlete.sport_id)
        )
    )
    if existing_athlete.scalar():
        raise ResponseError(
            status=status.HTTP_400_BAD_REQUEST,
            message="Спортсмен с таким ID уже существует",
        )
    try:
        athlete_instance = Athlete(**athlete.model_dump())
        session.add(athlete_instance)
        await session.commit()
        return athlete_instance
    except IntegrityError as e:
        # Если указаны неверные данные
        await session.rollback()
        raise ResponseError(
            status=status.HTTP_400_BAD_REQUEST,
            message=f"Проверьте вводимые данные",
            e=e,
        )
    except Exception as e:
        await session.rollback()
        raise ResponseError(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f" Ошибка: {e}", e=e
        )


async def get_athlete(id: int, session: AsyncSession) -> Type[Athlete]:
    """Получение данных о спортсмене по id"""

    athlete = await session.get(Athlete, id)
    if athlete is None:
        raise ResponseError(
            status=status.HTTP_404_NOT_FOUND,
            message="Спортсмен с указанным id не найден",
        )
    return athlete
