.PHONY: setup website clean

setup:
	uv sync

website: setup
	uv run jlconnor-github-io

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
