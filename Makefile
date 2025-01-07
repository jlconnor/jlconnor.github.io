.PHONY: setup website clean

setup:
	uv pip install -r requirements.txt

website: setup
	python script/gen.py

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
