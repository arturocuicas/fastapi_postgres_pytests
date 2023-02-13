
dev:
	@docker compose -f docker-compose.yaml up --build

run:
	@docker compose -f docker-compose.yaml up --build -d

down:
	@docker compose -f ./docker-compose.yaml down --remove-orphans

shell: run
	@docker exec -it fastapi_service bash

tests: run
	@docker exec -it fastapi_service poetry run pytest

.PHONY: dev run stop shell tests