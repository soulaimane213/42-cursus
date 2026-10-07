MAIN = a_maze_ing.py
CONFIG = config.txt
PACKAGE = amaze

install:
	pip install -r requirements.txt


run:
	python3 $(MAIN) $(CONFIG)

debug:
	python3 -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +

lint:
	flake8 .
	mypy . --explicit-package-bases --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --explicit-package-bases --strict

build:
	pip install build
	python3 -m build

.PHONY: install run debug clean lint lint-strict build
