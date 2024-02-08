from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.exceptions import ResponseError
from src.tournaments.models import Tournament
from src.tournaments.schemas import (
    AthleteOnTournamentsResponse,
    TournamentCreate,
    TournamentResponseCreate,
    TournamentResponseList,
)
from src.tournaments.service import TournamentCRUD

router = APIRouter(prefix="/tournaments", tags=["tournaments"])



@router.get("/", response_model=list[TournamentResponseList])
async def get_athletes_handler(session: AsyncSession = Depends(get_async_session)):
    """Получение данных всех спортсменов"""

    try:
        tournaments: list[Tournament] = (
            await TournamentCRUD.get_tournaments_with_athletes(session=session)
        )
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
                    sport_id=tournament.sport_id,
                    name=tournament.name,
                    athletes=athletes_responses,
                )
            )

        return tournaments_responses
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")


@router.post("/", response_model=TournamentResponseCreate)
async def create_tournament_handler(
    tournament_data: TournamentCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Добавление данных спортсмена в БД"""

    try:
        tournament: Tournament = await TournamentCRUD.create_tournament(
            tournament_data=tournament_data, session=session
        )
        tournament_response: TournamentResponseCreate = TournamentResponseCreate(
            id=tournament.id,
            datetime=tournament.datetime,
            sport_id=tournament.sport_id,
            name=tournament.name,
        )
        return tournament_response
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")
