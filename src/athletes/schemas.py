from pydantic import BaseModel


class AthleteResponseOne(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    country: str
    sport_name: str


class AthleteResponseCreate(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    country: str
    sport_id: int


class AthleteResponseList(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    country: str
    sport_name: str


class AthleteCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    country: str
    sport_id: int
