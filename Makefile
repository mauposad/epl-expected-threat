PYTHON ?= python
NOTEBOOKS := $(sort $(wildcard notebooks/*.ipynb))

.PHONY: help install data notebooks test lint format all

help:  ## Show available targets
	@grep -E '^[a-z]+:.*##' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-10s %s\n", $$1, $$2}'

install:  ## Install the package with analysis and dev extras (editable)
	$(PYTHON) -m pip install -e ".[analysis,dev]"

data:  ## Download StatsBomb data (if missing) and build all tables
	$(PYTHON) -m epl_xt.pipeline

notebooks:  ## Re-execute every notebook in place (regenerates reports/figures)
	$(PYTHON) -m nbconvert --to notebook --execute --inplace $(NOTEBOOKS)

test:  ## Run the unit tests
	$(PYTHON) -m pytest

lint:  ## Lint and check formatting
	$(PYTHON) -m ruff check src tests
	$(PYTHON) -m ruff format --check src tests

format:  ## Auto-format the code
	$(PYTHON) -m ruff format src tests
	$(PYTHON) -m ruff check --fix src tests

all: data notebooks  ## Rebuild everything from scratch
