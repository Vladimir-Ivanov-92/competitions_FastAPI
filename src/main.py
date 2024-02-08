from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.config import REDIS_HOST, REDIS_PORT
from src.athletes.router import router as router_athletes
from src.tournaments.router import router as router_competitions

from redis import asyncio as aioredis


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", encoding="utf8")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="Competitions App", lifespan=lifespan)

# Добавление роутеров приложений к основному app
app.include_router(router_competitions)
app.include_router(router_athletes)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
