from typing import Type

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.athletes.models import Athlete
from src.athletes.schemas import AthleteCreate, AthleteResponse
from src.athletes.service import AthleteCRUD
from src.database import get_async_session
from src.exceptions import ResponseError

router = APIRouter(prefix="/athletes", tags=["athletes"])


@router.get("/", response_model=list[AthleteResponse])
async def get_athletes_handler(session: AsyncSession = Depends(get_async_session)):
    """Получение данных всех спортсменов"""

    try:
        athlete: list[Athlete] = await AthleteCRUD.get_athletes(session=session)
        return athlete
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")


@router.post("/", response_model=AthleteResponse)
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


@router.get("/{athlete_id}", response_model=AthleteResponse)
async def get_athlete_handler(
    athlete_id: int, session: AsyncSession = Depends(get_async_session)
):
    """Получение данных о спортсмене по id"""

    try:
        athlete: Type[Athlete] = await AthleteCRUD.get_athlete(id=athlete_id, session=session)
        return athlete
    except ResponseError as e:
        raise HTTPException(status_code=e.status, detail=f"{e.message}")
