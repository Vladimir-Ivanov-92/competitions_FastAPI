from fastapi import FastAPI

from src.competitions.router import router as router_competitions

app = FastAPI(title="Competitions App")

app.include_router(router_competitions)


@app.get("/")
def read_root():
    return {"Hello": "World"}  # TODO Удалить!
