# LLMAid Testing Architecture

This document describes the testing architecture and setup for the LLMAid project.

## Overview

The testing architecture for LLMAid is designed to provide comprehensive coverage of the library's functionality while following Test-Driven Development (TDD) principles. The tests are organized around the specifications defined in the `specs/` directory and implement the behaviors described in the `docs/Public API Reference.md`.

## Test Structure

### Test Files

- **`test_hello_world.py`** - Basic "hello world" tests that verify the core infrastructure is working. These tests ensure that imports work, basic instantiation functions, and the main API methods exist.

### Test Fixtures

The `conftest.py` file provides shared fixtures:

- **`clean_env`** - Provides a clean environment without LLMAID environment variables
- **`mock_env`** - Sets up mock environment variables for testing
- **`basic_llmaid`** - Provides a basic LLMAid instance for testing
- **`templated_llmaid`** - Provides an LLMAid instance with a basic template
- **`temp_prompt_dir`** - Creates a temporary directory with sample prompt files

## Running Tests

### Using the Test Runner

The project includes a convenient test runner script `run_tests.py`:

```bash
# Run all tests
/path/to/.venv/bin/python run_tests.py test

# Run linting
/path/to/.venv/bin/python run_tests.py lint

# Format code
/path/to/.venv/bin/python run_tests.py format

# Run type checking
/path/to/.venv/bin/python run_tests.py typecheck

# Run all checks (format, lint, typecheck, tests)
/path/to/.venv/bin/python run_tests.py all
```

### Direct pytest Commands

You can also run tests directly with pytest:

```bash
# Run all tests
/path/to/.venv/bin/python -m pytest tests/ -v

# Run specific test file
/path/to/.venv/bin/python -m pytest tests/test_hello_world.py -v

# Run with coverage
/path/to/.venv/bin/python -m pytest tests/ --cov=src/llmaid

# Run tests matching a pattern
/path/to/.venv/bin/python -m pytest tests/ -k "test_config"
```

## Test Development Guidelines

### Test Naming

- Test methods should be descriptive and follow the pattern `test_<functionality>_<scenario>`
- Test classes should group related functionality (e.g., `TestConfiguration`, `TestCompletion`)

### Test Structure

Tests follow the Given-When-Then structure where applicable:

```python
def test_environment_variable_fallback(self, clean_env):
    """
    Scenario: Default instantiation with environment variables
    Given the environment variable LLMAID_BASE_URL is set to "http://localhost:8080"
    When I create an llmaid instance with no parameters
    Then the instance should have base_url "http://localhost:8080"
    """
    # Given - setup
    os.environ["LLMAID_BASE_URL"] = "http://localhost:8080"
    
    # When - action
    instance = llmaid.llmaid()
    
    # Then - assertion
    assert instance.base_url == "http://localhost:8080"
```

Always create one test for each scenario described in the specifications. Each test should be independent and not rely on the state of other tests.

### Async Tests

Async tests are marked with `@pytest.mark.asyncio`:

```python
@pytest.mark.asyncio
async def test_async_completion_exists(self):
    """Test that async completion method exists and works."""
    instance = llmaid.llmaid()
    response = await instance.acompletion("Hello async world")
    assert isinstance(response, str)
```

### Mock Strategy

You may only mock HTTP responses using HTTP mocking using `pytest-httpx`.
