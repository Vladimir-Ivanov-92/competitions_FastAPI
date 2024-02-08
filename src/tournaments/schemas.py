from datetime import datetime

from pydantic import BaseModel


class Tournament(BaseModel):
    datetime: datetime
    sport_id: int
    name: str


class AthleteWithPlace(BaseModel):
    athlete_id: int
    place: int


class TournamentCreate(BaseModel):
    tournament: Tournament
    athletes_with_place: list[AthleteWithPlace]


class TournamentResponseCreate(BaseModel):
    id: int
    datetime: datetime
    sport_id: int
    name: str


class AthleteOnTournamentsResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    country: str
    place: int


class TournamentResponseList(BaseModel):
    id: int
    datetime: datetime
    sport_id: str
    name: str
    athletes: list[AthleteOnTournamentsResponse]
