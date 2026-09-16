install:
	pip install flake8 mypy build

run: 
	python3 a_maze_ing.py config.txt

debug: 
	python3 -m pdb a_maze_ing.py config.txt 

clean: 
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@rm -rf .mypy_cache
	@rm -rf dist 
	@rm -rf src/mazegen.egg-info
	@echo "Done"


lint:
	@flake8 .
	@mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@flake8 .
	@mypy . --strict

.PHONY: run install debug clean lint lint-strict
