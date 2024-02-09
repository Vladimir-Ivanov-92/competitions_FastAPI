from httpx import AsyncClient

user_1_create = {
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "age": 18,
    "country": "Russia",
    "sport_id": 1,
}

user_1 = {
    "id": 1,
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "age": 18,
    "country": "Russia",
    "sport_name": "rowing",
}

user_2_create = {
    "first_name": "Kirill",
    "last_name": "kirillov",
    "age": 21,
    "country": "Russia",
    "sport_id": 1,
}

user_2 = {
    "id": 2,
    "first_name": "Kirill",
    "last_name": "kirillov",
    "age": 21,
    "country": "Russia",
    "sport_name": "rowing",
}


async def test_create_sport_with_async_client(async_client: AsyncClient):
    """Успешное добавление вида спорта"""
    data = {"name": "rowing"}
    response_data = {"id": 1, "name": "rowing"}
    response = await async_client.post("/athletes/sport", json=data)
    assert response.status_code == 201
    assert response.json() == response_data


async def test_create_athlete_handler(async_client: AsyncClient):
    """Успешное добавление спортсмена"""

    response_data = {
        "id": 1,
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "age": 18,
        "country": "Russia",
        "sport_id": 1,
    }
    response = await async_client.post("/athletes/", json=user_1_create)
    assert response.status_code == 201
    assert response.json() == response_data


async def test_create_athlete_handler_fail(async_client: AsyncClient):
    """Повторное добавление спортмена уже имеющегося в БД"""

    response = await async_client.post("/athletes/", json=user_1_create)
    assert response.status_code == 400


async def test_get_athlete_handler(async_client: AsyncClient):
    """Получение данных о спортсмене по ID"""
    response_data = {
        "id": 1,
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "age": 18,
        "country": "Russia",
        "sport_name": "rowing",
    }

    response = await async_client.get("/athletes/1")
    assert response.status_code == 200
    assert response.json() == response_data


async def test_get_athlete_handler_fail(async_client: AsyncClient):
    """Получение данных о спортсмене по ID, которого нет в БД"""
    response_data = {"detail": "Спортсмен с указанным id не найден"}

    response = await async_client.get("/athletes/2")
    assert response.status_code == 404
    assert response.json() == response_data


async def test_get_athletes_handler(async_client: AsyncClient):
    """Получение списка всех спортсменов"""
    response_data = [user_1, user_2]

    await async_client.post("/athletes/", json=user_2_create)

    response = await async_client.get("/athletes/")
    assert response.status_code == 200
    assert response.json() == response_data
