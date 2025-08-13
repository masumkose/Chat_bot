.PHONY: up down clean logs rebuild

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

rebuild:
	docker compose build --no-cache

clean:
	docker compose down -v --remove-orphans
	docker system prune -f
	docker volume prune -f
