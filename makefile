.PHONY: install run test lint format type db-init db-migrate add-dummyUsers

install:
	uv sync

run:
	uv run flask --app app:create_app --debug run --host 127.0.0.1 --port 5000

test:
	uv run pytest

format:
	uv run --group format black .
	uv run --group format ruff format

lint:
	uv run --group lint flake8 .
	uv run --group type mypy .

db-init:
	uv run flask --app app:create_app db init

# Usage: make db-migrate MSG="add users table"
db-migrate:
	@if [ -z "$(MSG)" ]; then echo "MSG is required. Example: make db-migrate MSG='add users table'"; exit 1; fi
	uv run flask --app app:create_app db migrate -m "$(MSG)"
	uv run flask --app app:create_app db upgrade

add-dummyUsers:
	@if [-z $(N)]; then echo "N is required. Example: make add-dummyUsers N=50"; exit 1; fi
	# Ensure DB is migrated first
	uv run flask --app app:create_app db upgrade
	# Seed dummy rows
	uv run flask --app app:create_app seed-db --users $(N)
