# Competitions_API

Приложение предоставляюще api для сохранения результатов турниров по различным видам спорта с 
указанием участников турниров и занятых ими мест.

### В данном проекте использовались следующие инструменты:

- python v3.11
- fastapi v0.109.2
- sqlalchemy v2.0.25
- alembic v1.13.1
- asyncpg v0.29
- uvicorn v^0.27
- gunicorn v21.2
- redis v5.0.1
- requests v2.31
- fastapi-cache2 v0.2.1

```
get("/tournaments/") - список всех турниров c указанием участников 
 каждого турнира и занятых ими мест (в порядке убывания)

Response:
[
  {
    "id": int,
    "datetime": datetime,
    "sport_id": str,
    "name": str,
    "athletes": [
      {
        "id": int,
        "first_name": str,
        "last_name": str,
        "country": str,
        "place": int
      }
    ]
  }
]
```

```
post("/tournaments/") - Добавление данных о турнире в БД

Request: 
{
  "tournament": {
    "datetime": datetime,
    "sport_id": int,
    "name": str
  },
  "athletes_with_place": [
    {
      "athlete_id": int,
      "place": int
    }
  ]
}

Response:
{
  "id": int,
  "datetime": str,
  "sport_id": int,
  "name": str
}
```

```
get("/tournaments/{year}/{month}") - Получение данных всех турниров 
с фильтром по переданным данным (год, месяц)

Response:
[
  {
    "id": int,
    "datetime": datetime,
    "sport_id": str,
    "name": str,
    "athletes": [
      {
        "id": int,
        "first_name": str,
        "last_name": str,
        "country": "str,
        "place": int
      }
    ]
  }
]
```

```
get("/athletes/") - Получение данных всех спортсменов
Response:
[
  {
    "id": int,
    "first_name": str,
    "last_name": str,
    "age": int,
    "country": str,
    "sport_name": str
  }
]
```

```
post("/athletes/") - Добавление данных спортсмена в БД

Request: 
{
  "first_name": str,
  "last_name": str,
  "age": int,
  "country": str,
  "sport_id": int
}
        
Response:
{
  "id": int,
  "first_name": str,
  "last_name": str,
  "age": int,
  "country": str,
  "sport_id": int
}
```

```
get("/athletes/{athlete_id}") - Получение данных о спортсмене по id
Response:
{
  "id": int,
  "first_name": str,
  "last_name": str,
  "age": int,
  "country": str,
  "sport_name": str
}
```

```
post("/athletes/sport") - Добавление нового вида спорта в БД

Request: 
{
  "name": str
}
        
Response:
{
  "id": int,
  "name": str
}
```

В приложении используется кэширование для некоторых обработчиков с помщью redis и библиотеки 
fastapi-cache2:
```python
@router.get("/{year}/{month}", response_model=list[TournamentResponseList])
@cache(expire=EXPIRE)
async def get_tournaments_filter_year_month()
...
```

## Настройка и запуск:

Перейдите в директорию, в которую будете клонировать репозиторий. 
Необходимо наличие установленного и запущенного Docker.
Для скачивания репозитория и разворачивания проекта локально в docker контейнере 
(создание БД, запуск приложения):

git clone https://github.com/Vladimir-Ivanov-92/DRF_API_Exchange_Rate.git

Необходимо создать в текущей директории .env файл 
и заполнить данными по образцу .env.example

Для автоматизации сборки проекта в репозитории размещен Makefile. Для запуска приложения
выполните: 

```
make up  - создаст Docker контейнеры "app" "db" "redis" и запустит приложение 
с помощью gunicorn

make migrate"- выполнит миграции БД

make down -  остановит и удалит все созданные контейнеры
```