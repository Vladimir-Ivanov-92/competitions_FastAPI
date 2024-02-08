from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.exceptions import ResponseError
from src.tournaments.models import Tournament
from src.tournaments.schemas import TournamentCreate, TournamentResponseCreate
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


@router.get("/")
async def get_competitions_from_month():
    """Получение результатов турниров за определенный месяц"""
    return data


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
            id=tournament.id, datetime=tournament.datetime, sport_id=tournament.sport_id
        )
        return tournament_response
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")
