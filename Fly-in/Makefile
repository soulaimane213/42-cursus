ARGS ?= map.txt

.PHONY: all install run debug clean lint lint-strict

all: run

install:
	pip install flake8 mypy || python3 -m pip install flake8 mypy || true

run:
	python3 main.py $(ARGS)

debug:
	python3 -m pdb main.py $(ARGS)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true

lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict