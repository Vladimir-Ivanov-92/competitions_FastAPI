from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.athletes.models import Athlete
from src.database import get_async_session
from src.exceptions import ResponseError
from src.tournaments.models import Tournament
from src.tournaments.schemas import TournamentCreate, TournamentResponseCreate, TournamentResponseList, \
    AthleteOnTournamentsResponse
from src.tournaments.service import TournamentCRUD

router = APIRouter(prefix="/tournaments", tags=["tournaments"])

# TODO: Удалить тестовые данные (data)!
data = {
    "year": 2023,
    "month": 1,
    "sport": "rowing",
    "number_of_competitions": 2,
    "tournaments": [
        {
            "index": 1,
            "competition_id": 1,
            "competition_datetime": "2023-01-15",
            "number_all_athlets": 5,
            "results": [
                {
                    "place": 1,
                    "athlets_id": 3,
                    "name": "Ivan",
                    "surname": "Ivanovich",
                    "country": "Russia",
                },
                {
                    "place": 2,
                    "athlets_id": 1,
                    "name": "Petr",
                    "surname": "Petrovich",
                    "country": "Russia",
                },
                {
                    "place": 3,
                    "athlets_id": 2,
                    "name": "Stepan",
                    "surname": "Stepanovich",
                    "country": "Belarus",
                },
            ],
        }
    ],
}


@router.get("/", response_model=list[TournamentResponseList])
async def get_athletes_handler(session: AsyncSession = Depends(get_async_session)):
    """Получение данных всех спортсменов"""

    try:
        tournaments: list[Tournament] = await TournamentCRUD.get_tournaments_with_athletes(session=session)
        tournaments_responses: list[TournamentResponseList] = []
        for tournament in tournaments: # type: Athlete
            athletes_responses = [
                AthleteOnTournamentsResponse(
                    id=athlete.id,
                    first_name=athlete.first_name,
                    last_name=athlete.last_name,
                    country=athlete.country,

                )
                for athlete in tournament.athletes
            ]

            tournaments_responses.append(
                TournamentResponseList(
                    id=tournament.id,
                    datetime=tournament.datetime,
                    sport_id=tournament.sport_id,
                    name=tournament.name,
                    athletes=athletes_responses
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
            id=tournament.id, datetime=tournament.datetime, sport_id=tournament.sport_id, name=tournament.name
        )
        return tournament_response
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")
