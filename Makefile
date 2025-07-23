# LLMAid Makefile
# Convenient commands for development and testing

# Variables
VENV_PATH = .venv/bin
PYTHON = $(VENV_PATH)/python
PIP = $(VENV_PATH)/pip

# Default target
.PHONY: help
help:
	@echo "LLMAid Development Commands"
	@echo "=========================="
	@echo ""
	@echo "Setup:"
	@echo "  install     Install project in development mode"
	@echo "  install-dev Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test        Run all tests"
	@echo "  test-hello  Run hello world tests only"
	@echo "  test-watch  Run tests in watch mode"
	@echo ""
	@echo "Code Quality:"
	@echo "  format      Format code with black"
	@echo "  lint        Run linting with flake8"
	@echo "  typecheck   Run type checking with mypy"
	@echo "  check-all   Run format, lint, typecheck, and tests"
	@echo ""
	@echo "Utilities:"
	@echo "  clean       Clean up temporary files"
	@echo "  coverage    Run tests with coverage report"

# Setup targets
.PHONY: install
install:
	$(PIP) install -e .

.PHONY: install-dev
install-dev:
	$(PIP) install -e ".[dev]"

# Testing targets
.PHONY: test
test:
	$(PYTHON) -m pytest tests/ -v

.PHONY: test-hello
test-hello:
	$(PYTHON) -m pytest tests/test_hello_world.py -v

.PHONY: test-watch
test-watch:
	$(PYTHON) -m pytest tests/ -v --tb=short -f

.PHONY: coverage
coverage:
	$(PYTHON) -m pytest tests/ --cov=src/llmaid --cov-report=html --cov-report=term

# Code quality targets
.PHONY: format
format:
	$(VENV_PATH)/black src/ tests/

.PHONY: lint
lint:
	$(VENV_PATH)/flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503

.PHONY: typecheck
typecheck:
	$(VENV_PATH)/mypy src/llmaid/

.PHONY: check-all
check-all: format lint typecheck test

# Utility targets
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage

# Development helper - run hello world test quickly
.PHONY: hello
hello: test-hello
