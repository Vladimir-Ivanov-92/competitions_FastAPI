import uvicorn
from fastapi import FastAPI

from src.athletes.router import router as router_athletes
from src.competitions.router import router as router_competitions

app = FastAPI(title="Competitions App")

# Добавление роутеров приложений к основному app
app.include_router(router_competitions)
app.include_router(router_athletes)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
