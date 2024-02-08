from asyncio import sleep

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import EXPIRE
from src.database import get_async_session
from src.exceptions import ResponseError
from src.tournaments.models import Tournament
from src.tournaments.schemas import (
    TournamentCreate,
    TournamentResponseCreate,
    TournamentResponseList,
)
from src.tournaments.service import TournamentCRUD

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


@router.get("/", response_model=list[TournamentResponseList])
@cache(expire=EXPIRE)
async def get_tournaments_handler(session: AsyncSession = Depends(get_async_session)):
    """Получение данных всех турниров"""

    try:
        tournaments: list[Tournament] = (
            await TournamentCRUD.get_tournaments_with_athletes(session=session)
        )

        tournaments_responses = await TournamentCRUD.to_response_format(tournaments)

        return tournaments_responses
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")


@router.get("/{year}/{month}", response_model=list[TournamentResponseList])
@cache(expire=EXPIRE)
async def get_tournaments_filter_year_month(
        year: int, month: int, session: AsyncSession = Depends(get_async_session)
):
    """Получение данных всех турниров с фильтром по (год, месяц)"""

    try:
        tournaments: list[Tournament] = (
            await TournamentCRUD.get_tournaments_filter_year_month(
                year=year, month=month, session=session
            )
        )

        tournaments_responses = await TournamentCRUD.to_response_format(tournaments)

        await sleep(3)  # TODO DEL

        return tournaments_responses
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")


@router.post("/", response_model=TournamentResponseCreate)
async def create_tournament_handler(
        tournament_data: TournamentCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """Добавление данных о турнире в БД"""

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
