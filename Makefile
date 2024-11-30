.DEFAULT_GOAL := help

# Use this sed command to parse the Makefile for targets and descriptions
# The comment directly above the target is used as the description
help:
	@sed -n 's/^## //p' $(MAKEFILE_LIST) | column -t -s ':' | sed -e 's/^/ /'

# Directories
SRC_DIRS := src
TEST_DIRS := tests

# Xenon configuration
XENON_MAX_ABSOLUTE := B
XENON_MAX_MODULES := B
XENON_MAX_AVERAGE := B

## install: Install necessary dependencies and set up hooks.
install:
	@ poetry install  # Install Python dependencies using Poetry
	@ pre-commit install  # Set up Git pre-commit hooks
	@ gitlint install-hook  # Install Gitlint hook for linting commits

## lint-check: Lint source files without modifying them.
lint-check:
	@ ruff check $(SRC_DIRS)

## lint-fix: Format and fix linting issues in source files.
lint-fix:
	@ ruff check $(SRC_DIRS) --fix
	@ ruff format $(SRC_DIRS)

## lint-check-tests: Lint test files without modifying them.
lint-check-tests:
	@ ruff check $(TEST_DIRS)

## lint-fix-tests: Format and fix linting issues in test files.
lint-fix-tests:
	@ ruff check $(TEST_DIRS) --fix
	@ ruff format $(TEST_DIRS)

## cc: Calculate Cyclomatic Complexity.
cc:
	# Calculating cyclomatic complexity using radon
	@ radon cc $(SRC_DIRS) -s

	# Ensuring code complexity adheres to standards using xenon
	@ xenon --max-absolute $(XENON_MAX_ABSOLUTE) \
	       --max-modules $(XENON_MAX_MODULES) \
	       --max-average $(XENON_MAX_AVERAGE) $(SRC_DIRS)

## test: Run tests with coverage
test:
	set -e &&export ENVIRONMENT='test' && coverage run -m pytest --capture=no --ff $(extra) && coverage report

## test-cov: Run tests and generate a coverage report.
test-cov:
	set -e &&export ENVIRONMENT='test' && coverage run -m pytest --capture=no &&coverage report	&&coverage html

## dev: Run the development server.
dev:
	set -e &&export ENVIRONMENT='dev' && uvicorn $(SRC_DIRS).application.api:app --host 0.0.0.0 --reload

## prod: Run as prod server.
prod:
	set -e &&export ENVIRONMENT='prod' && uvicorn $(SRC_DIRS).application.api:app --host 0.0.0.0 --reload

## staging: Run as stage server.
staging:
	set -e &&export ENVIRONMENT='staging' && uvicorn $(SRC_DIRS).application.api:app --host 0.0.0.0 --reload


.PHONY: install lint-check lint-fix lint-check-tests lint-fix-tests cc test test-cov dev prod stage help
