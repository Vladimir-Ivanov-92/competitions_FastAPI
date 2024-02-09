from httpx import AsyncClient

from tests.test_athletes import user_1_create, user_2_create

tournament_1_create = {
    "tournament": {
        "datetime": "2023-01-01T12:00:00",
        "sport_id": 1,
        "name": "Tornament_1",
    },
    "athletes_with_place": [
        {"athlete_id": 1, "place": 2},
        {"athlete_id": 2, "place": 1},
    ],
}


async def test_create_tournament_handler(async_client: AsyncClient):
    """Успешное добавление данных по турниру"""

    response_data = {
        "datetime": "2023-01-01T12:00:00",
        "id": 1,
        "name": "Tornament_1",
        "sport_id": 1,
    }

    # Добавляем спорт rowing в БД
    await async_client.post("/athletes/sport", json={"name": "rowing"})
    # Добавляем двух спортсменов
    await async_client.post("/athletes/", json=user_1_create)
    await async_client.post("/athletes/", json=user_2_create)

    response = await async_client.post("/tournaments/", json=tournament_1_create)
    assert response.status_code == 201
    assert response.json() == response_data


async def test_create_tournament_handler_fail(async_client: AsyncClient):
    """Повторное добавление турнира, уже существующего в БД"""

    response = await async_client.post("/tournaments/", json=tournament_1_create)
    assert response.status_code == 400


async def test_get_tournaments_handler(async_client: AsyncClient):
    """Получение данных всех турниров в БД"""

    response_data = [
        {
            "datetime": "2023-01-01T12:00:00",
            "id": 1,
            "name": "Tornament_1",
            "sport_id": "rowing",
            "athletes": [
                {
                    "country": "Russia",
                    "first_name": "Kirill",
                    "id": 2,
                    "last_name": "kirillov",
                    "place": 1,
                },
                {
                    "country": "Russia",
                    "first_name": "Ivan",
                    "id": 1,
                    "last_name": "Ivanov",
                    "place": 2,
                },
            ],
        }
    ]

    response = await async_client.get("/tournaments/")
    assert response.status_code == 200
    assert response.json() == response_data
