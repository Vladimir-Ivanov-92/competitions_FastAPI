from datetime import datetime
from typing import Sequence

from sqlalchemy import select, Result, Row
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from src.athletes.models import Athlete
from src.exceptions import ResponseError
from src.tournaments.models import Tournament
from src.tournaments.schemas import TournamentCreate


class TournamentCRUD:
    """Содержит методы для CRUD операций с объектами Tournament"""

    @staticmethod
    async def get_tournaments_with_athletes(
            session: AsyncSession,
    ) -> list[Tournament]:

        try:
            query = (
                select(Tournament)
                .options(selectinload(Tournament.athletes))
                .order_by(Tournament.id)
            )
            result = await session.execute(query)
            tournaments: list[Tournament] = list(result.scalars().all())
            return tournaments
        except Exception as e:
            raise ResponseError(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f" Ошибка: {e}",
                e=e,
            )

    @staticmethod
    async def create_tournament(
            tournament_data: TournamentCreate,
            session: AsyncSession,
    ) -> Tournament:
        """Добавление данных по турниру в БД"""

        # Проверяем, существует ли уже турнир с таким же именем в БД
        existing_tournament = await session.execute(
            select(Tournament).where(
                (Tournament.name == tournament_data.tournament.name)
            )
        )
        if existing_tournament.scalar():
            raise ResponseError(
                status=status.HTTP_400_BAD_REQUEST,
                message="Турнир с таким названием уже существует",
            )
        try:
            # Добавление в БД объекта Tournament с переданными данными
            tournament = Tournament(**tournament_data.tournament.model_dump())
            session.add(tournament)
            await session.commit()

            # Получение созданного объекта Tournament по ID
            tournament_for_add_athlete = await session.scalar(
                select(Tournament)
                .where(Tournament.id == tournament.id)
                .options(
                    selectinload(Tournament.athletes),
                ),
            )
            # Получение последовательности строк участвующих в турнире спортменов
            athletes_query = select(Athlete).filter(Athlete.id.in_(tournament_data.lst_athletes_id))
            result: Result = await session.execute(athletes_query)
            athletes: Sequence[Row] = result.scalars().all()

            # Добавление в ассоциативную таблицу спортсменов участвующих в турнире
            tournament_for_add_athlete.athletes.extend(athletes)
            await session.commit()

            return tournament
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f" Ошибка: {e}",
                e=e,
            )
