VENV := .venv
BIN_DIR := $(VENV)/bin
PYTHON := $(BIN_DIR)/python
FLAKE := $(BIN_DIR)/flake8
MYPY := $(BIN_DIR)/mypy
PYLINT := $(BIN_DIR)/pylint
UV := uv
SRC := codes
ARGS ?= "maps/test_map/test_map2.txt"


install:
	$(UV) sync

run:
	$(UV) run $(PYTHON) $(SRC) \
		--input $(ARGS)

visual:
	$(UV) run $(PYTHON) $(SRC) \
		--visual --input $(ARGS)

flake:
	$(UV) run $(PYTHON) $(FLAKE) $(SRC)

lint: flake
	$(UV) run $(PYTHON) $(MYPY) $(SRC)

lint-strict: flake
	$(MYPY) $(SRC) --strict

pylint:
	$(PYLINT) $(SRC)

docstring: flake
	$(DOCSTRING) $(SRC)

debug:
	uv run python -m pdb codes/__main__.py

list:
	$(UV) pip list

clean:
	find . -name "*.pyc" -exec rm -rf {} +
	find . -type d \( -name "__pycache__" -o -name ".mypy_cache" \) -exec rm -rf {} +

fclean: clean
	rm -rf $(VENV)

re: fclean install

.PHONY = install run flake mypy re clean fclean list debug visual
