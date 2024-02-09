from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.athletes.models import Athlete, Sport
from src.athletes.schemas import (
    AthleteCreate,
    AthleteResponseCreate,
    AthleteResponseList,
    AthleteResponseOne,
    SportCreate,
    SportResponse,
)
from src.athletes.service import AthleteCRUD
from src.database import get_async_session
from src.exceptions import ResponseError

router = APIRouter(prefix="/athletes", tags=["athletes"])


@router.get("/", response_model=list[AthleteResponseList])
async def get_athletes_handler(session: AsyncSession = Depends(get_async_session)):
    """Получение данных всех спортсменов"""

    try:
        athletes: list[Athlete] = await AthleteCRUD.get_athletes(session=session)
        athletes_responses: list[AthleteResponseList] = [
            AthleteResponseList(
                id=athlete.id,
                first_name=athlete.first_name,
                last_name=athlete.last_name,
                age=athlete.age,
                country=athlete.country,
                sport_name=athlete.sport.name,
            )
            for athlete in athletes
        ]
        return athletes_responses
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")


@router.get("/{athlete_id}", response_model=AthleteResponseOne)
async def get_athlete_handler(
    athlete_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Получение данных о спортсмене по id"""

    try:
        athlete: Athlete = await AthleteCRUD.get_athlete(id=athlete_id, session=session)
        athlete_responses: AthleteResponseOne = AthleteResponseOne(
            id=athlete.id,
            first_name=athlete.first_name,
            last_name=athlete.last_name,
            age=athlete.age,
            country=athlete.country,
            sport_name=athlete.sport.name,
        )
        return athlete_responses
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")


@router.post("/", response_model=AthleteResponseCreate, status_code=201)
async def create_athlete_handler(
    athlete: AthleteCreate, session: AsyncSession = Depends(get_async_session)
):
    """Добавление данных спортсмена в БД"""

    try:
        athlete_instance: Athlete = await AthleteCRUD.create_athlete(
            athlete=athlete, session=session
        )
        return athlete_instance
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")


@router.post("/sport", response_model=SportResponse, status_code=201)
async def create_sport_handler(
    sport: SportCreate, session: AsyncSession = Depends(get_async_session)
):
    """Добавление нового вида спорта в БД"""

    try:
        sport = Sport(**sport.model_dump())
        session.add(sport)
        await session.commit()
        return sport
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e=}")
