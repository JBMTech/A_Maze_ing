# ¡¡Todavia no se si funciona estos commandos, se realizaran test!!
# VARIABLES
PYTHON = python3
MAIN = a_maze_ing.py
CONFIG = config.txt

VENV = matrix
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# CREAR ENTORNO
venv:
	python3 -m venv $(VENV)

# INSTALL
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install flake8 mypy

# RUN
run:
	$(PYTHON) a_maze_ing.py config.txt

# DEBUG
debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

# CLEAN
clean:
	rm -rf __pycache__ */__pycache__ *.pyc .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "matrix" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -f {} +

# LINT
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# LINT STRICT (OPCIONAL)
lint-strict:
	flake8 .
	mypy . --strict


.PHONY: venv install run debug clean lint lint-strict