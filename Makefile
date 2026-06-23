VENV := .venv
BIN_DIR := $(VENV)/bin
PYTHON := $(BIN_DIR)/python
FLAKE := $(BIN_DIR)/flake8
MYPY := $(BIN_DIR)/mypy
PYLINT := $(BIN_DIR)/pylint
UV := uv
SRC := codes
ARGS ?= "maps/easy/01_linear_path.txt"


install:
	@if [ -z "$(UV)" ]; then \
		@echo "intalling uv"; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
		export PATH="$$HOME/.local/bin/:$$PATH"; \
	fi
	$(UV) sync

run:
	$(UV) run $(PYTHON) $(SRC) \
		--input $(ARGS)

flake:
	$(FLAKE) $(SRC)

lint: flake
	$(MYPY) $(SRC)

pylint:
	$(PYLINT) $(SRC)

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

.PHONY = install run flake mypy re clean fclean list debug
