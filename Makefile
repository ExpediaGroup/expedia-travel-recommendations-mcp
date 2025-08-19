.PHONY: setup install format lint test build

setup:
	pip install --upgrade pipx
	pipx install uv==0.7.7 --force
	uv venv .venv

install: setup
	uv pip install -e .

format: setup
	uv pip install ruff black
	uv run ruff check examples/ expedia_travel_recommendations/ tests/ --fix
	uv run black examples/ expedia_travel_recommendations/ tests/

lint: setup
	uv pip install ruff black
	uv run ruff check .
	uv run black --check .

test: setup
	uv pip install pytest pytest-asyncio
	uv run pytest -q

build: setup
	uv build