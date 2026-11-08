.PHONY: help install run lint format clean

help:  ## Show available commands
	@grep -E '^[a-z-]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  make %-10s %s\n", $$1, $$2}'

install:  ## Install dependencies
	uv sync

run:  ## Run the demo script
	uv run python scripts/demo.py

lint:  ## Check code with ruff
	uv run ruff check .

format:  ## Format code with ruff
	uv run ruff format .

clean:  ## Remove caches and the virtual environment
	find . -name __pycache__ -not -path "./.venv/*" -prune -exec rm -rf {} +
	rm -rf .mypy_cache .ruff_cache
	rm -rf .venv/
