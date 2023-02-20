
coffee:
	@printf 'Enjoy your coffee! \xE2\x98\x95'

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

lint: run
	@docker exec -it fastapi_service poetry run black .
	@docker exec -it fastapi_service poetry run isort . --profile black

.PHONY: coffee dev run stop shell tests lint