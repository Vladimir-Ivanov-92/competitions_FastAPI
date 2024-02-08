up:
	docker compose -f docker-compose.yml up -d --build

down:
	docker compose -f docker-compose.yml down

migrate:
	docker exec -it app bash -c "alembic upgrade head"

