# VARIABLES
VENV = matrix
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

MAIN = a_maze_ing.py
CONFIG = config.txt

# CREAR ENTORNO
venv:
	python3 -m venv $(VENV)

# INSTALL
install: venv
	$(PIP) install --upgrade pip
# $(PIP) install -r requirements.txt
	$(PIP) install flake8 mypy

# RUN
run:
	$(PYTHON) $(MAIN) $(CONFIG)

# DEBUG
debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

# CLEAN
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# CLEAN VENV
clean-venv:
	rm -rf $(VENV)

# LINT
lint:
	$(VENV)/bin/flake8 $(MAIN) mazegen/*
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# LINT STRICT
lint-strict:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --strict

.PHONY: venv install run debug clean clean-venv lint lint-strict