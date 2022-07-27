current_dir = $(shell pwd)

lint:
	@echo 'lint TODO'

test:
	@echo 'test TODO'

dev: run_dev migrate_up

run_dev:
	docker-compose --project-name kaizen -f docker-compose.dev.yml up -d

migrate_up:
	docker run --rm -it --network=host -v "$(current_dir)/db:/db" \
		-e DATABASE_URL="postgres://postgres:postgres@127.0.0.1:5432/kaizen?sslmode=disable" \
		amacneil/dbmate up