from typing import Sequence

from sqlalchemy import Result, Row, extract, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from starlette import status

from src.athletes.models import Athlete
from src.exceptions import ResponseError
from src.tournaments.models import Tournament, TournamentAthleteAssociations
from src.tournaments.schemas import (
    AthleteOnTournamentsResponse,
    TournamentCreate,
    TournamentResponseList,
)


class TournamentCRUD:
    """Содержит методы для CRUD операций с объектами Tournament"""

    @staticmethod
    async def get_tournaments_with_athletes(
        session: AsyncSession,
    ) -> list[Tournament]:

        try:
            query = (
                select(Tournament)
                .options(
                    selectinload(Tournament.athletes_associations).joinedload(
                        TournamentAthleteAssociations.athlete
                    ),
                    joinedload(Tournament.sport),
                )
                .order_by(Tournament.id)
            )
            result = await session.execute(query)
            tournaments: list[Tournament] = list(result.scalars().all())

            # Сортировка спортсменов по месту в каждом турнире
            for tournament in tournaments:
                tournament.athletes_associations.sort(key=lambda x: x.place)

            return tournaments
        except Exception as e:
            raise ResponseError(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f" Ошибка: {e}",
                e=e,
            )

    @staticmethod
    async def get_tournaments_filter_year_month(
        session: AsyncSession,
        year: int,
        month: int,
    ) -> list[Tournament]:

        try:
            query = (
                select(Tournament)
                .options(
                    selectinload(Tournament.athletes_associations).joinedload(
                        TournamentAthleteAssociations.athlete
                    ),
                    joinedload(Tournament.sport),
                )
                .filter(
                    extract("year", Tournament.datetime) == year,
                    extract("month", Tournament.datetime) == month,
                )
                .order_by(Tournament.id)
            )
            result = await session.execute(query)
            tournaments: list[Tournament] = list(result.scalars().all())

            # Сортировка спортсменов по месту в каждом турнире
            for tournament in tournaments:
                tournament.athletes_associations.sort(key=lambda x: x.place)

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

            # Получение последовательности строк участвующих в турнире спортменов
            athletes_query = select(Athlete).filter(
                Athlete.id.in_(
                    [
                        athlete.athlete_id
                        for athlete in tournament_data.athletes_with_place
                    ]
                )
            )
            result: Result = await session.execute(athletes_query)
            athletes: Sequence[Row] = result.scalars().all()

            # Формируем список значений для вставки и добавляем значения в TournamentAthleteAssociations
            values = [
                {
                    "tournament_id": tournament.id,
                    "athlete_id": athlete.id,
                    "place": athlete_with_place.place,
                }
                for athlete, athlete_with_place in zip(
                    athletes, tournament_data.athletes_with_place
                )
            ]

            insert_statement = TournamentAthleteAssociations.__table__.insert().values(
                values
            )
            await session.execute(insert_statement)

            await session.commit()

            return tournament
        except IntegrityError as e:
            # Если указаны неверные данные
            await session.rollback()
            raise ResponseError(
                status=status.HTTP_400_BAD_REQUEST,
                message="Проверьте вводимые данные",
                e=e,
            )
        except Exception as e:
            await session.rollback()
            raise ResponseError(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                message=f" Ошибка: {e}",
                e=e,
            )

    @staticmethod
    async def to_response_format(
        tournaments: list[Tournament],
    ) -> list[TournamentResponseList]:
        tournaments_responses: list[TournamentResponseList] = []
        for tournament in tournaments:
            athletes_responses = [
                AthleteOnTournamentsResponse(
                    id=tournament_athletes_associations.athlete.id,
                    first_name=tournament_athletes_associations.athlete.first_name,
                    last_name=tournament_athletes_associations.athlete.last_name,
                    country=tournament_athletes_associations.athlete.country,
                    place=tournament_athletes_associations.place,
                )
                for tournament_athletes_associations in tournament.athletes_associations
            ]

            tournaments_responses.append(
                TournamentResponseList(
                    id=tournament.id,
                    datetime=tournament.datetime,
                    sport_id=tournament.sport.name,
                    name=tournament.name,
                    athletes=athletes_responses,
                )
            )
        return tournaments_responses
