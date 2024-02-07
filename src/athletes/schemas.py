from pydantic import BaseModel


class AthleteResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    age: int
    country: str
    sport_id: int


class AthleteCreate(BaseModel):
    first_name: str
    last_name: str
    age: int
    country: str
    sport_id: int
