from datetime import datetime

from pydantic import BaseModel


class Tournament(BaseModel):
    datetime: datetime
    sport_id: int
    name: str


class TournamentCreate(BaseModel):
    tournament: Tournament
    lst_athletes_id: list[int]


class TournamentResponseCreate(BaseModel):
    id: int
    datetime: datetime
    sport_id: int
    name: str
