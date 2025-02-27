start: env_file
	docker compose build
	docker compose up

env_file:
ifeq (,$(wildcard .env))
	@echo "Creating .env file from .example-env..."
	cp .example-env .env
endif

venv:
ifeq (,$(wildcard .venv))
	@echo "Creating .venv"
	python3.12 -m venv .venv
endif

test:
	source .venv/bin/activate && pip install -r requirements.txt && pytest