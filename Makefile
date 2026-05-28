
VENV = matrix
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

MAIN = a_maze_ing.py
CONFIG = config.txt
WHEEL = mazegen-1.0.0-py3-none-any.whl

GREEN=\033[0;32m
RED=\033[0;31m
NC=\033[0m


venv:
	python3 -m venv $(VENV)

# INSTALL
install: venv
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy build

	@if [ -x mazegen ]; then \
		printf "$(GREEN)Run mazegen$(NC)\n"; \
	else \
		printf "$(RED)Installed wheel local$(NC)\n"; \
		$(PIP) install "$(WHEEL)"; \
	fi

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
	rm -rf maze.txt dist/ mazegen.egg*

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

# BUILD PKG
build-pkg:
	$(PYTHON) -m build

.PHONY: venv install run debug clean clean-venv lint lint-strict build-pkg