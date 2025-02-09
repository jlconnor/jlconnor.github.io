.PHONY: setup website clean

setup:
	uv sync

website: setup
	python src/site.py ${HOME}/.local/share/Obsidian/Primary/Blog .
	# uv run jlconnor_github_io ${HOME}/.local/share/Obsidian/Primary/Blog .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
