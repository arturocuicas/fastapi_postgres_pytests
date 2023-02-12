
dev:
	@docker compose -f docker-compose.yaml up --build

run:
	@docker compose -f docker-compose.yaml up --build -d

down:
	@docker compose -f ./docker-compose.yaml down --remove-orphans

shell: run
	@docker exec -it fastapi_service bash

.PHONY: dev run stop shell