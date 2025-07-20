build:
	docker-compose build

up:
	docker-compose up

up-prod:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up

down:
	docker-compose down

logs:
	docker-compose logs -f

bash:
	docker-compose exec app bash