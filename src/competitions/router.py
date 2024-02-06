from fastapi import APIRouter

router = APIRouter(prefix="/competitions", tags=["competitions"])

# TODO: Удалить тестовые данные (data)!
data = {
    "year": 2023,
    "month": 1,
    "sport": "rowing",
    "number_of_competitions": 2,
    "competitions": [
        {
            "index": 1,
            "competition_id": 1,
            "competition_datetime": "2023-01-15",
            "number_all_athlets": 5,
            "results": [
                {
                    "place": 1,
                    "athlets_id": 3,
                    "name": "Ivan",
                    "surname": "Ivanovich",
                    "country": "Russia",
                },
                {
                    "place": 2,
                    "athlets_id": 1,
                    "name": "Petr",
                    "surname": "Petrovich",
                    "country": "Russia",
                },
                {
                    "place": 3,
                    "athlets_id": 2,
                    "name": "Stepan",
                    "surname": "Stepanovich",
                    "country": "Belarus",
                },
            ],
        }
    ],
}


@router.get("/")
async def get_competitions_from_month():
    """Получение результатов турниров за определенный месяц"""
    return data
