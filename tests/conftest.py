"""
Pytest configuration and shared fixtures for LLMAid tests.
"""

import pytest
import os
from unittest.mock import patch
from pathlib import Path
from typing import List

# Add the src directory to Python path for imports
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from llmaid import llmaid


@pytest.fixture
def clean_env():
    """Fixture that provides a clean environment without LLMAID env vars."""
    env_vars = [
        "LLMAID_BASE_URL",
        "LLMAID_SECRET",
        "LLMAID_MODEL",
        "LLMAID_PROMPT_DIR",
        "LLMAID_STRICT_TEMPLATE",
        "LLMAID_TEMPERATURE",
        "LLMAID_MAX_TOKENS",
        "LLMAID_CONTEXT_LENGTH",
        "LLMAID_TOP_P",
        "LLMAID_FREQUENCY_PENALTY",
        "LLMAID_PRESENCE_PENALTY",
    ]

    original_values = {}
    for var in env_vars:
        original_values[var] = os.environ.get(var)
        if var in os.environ:
            del os.environ[var]

    yield

    # Restore original environment
    for var, value in original_values.items():
        if value is not None:
            os.environ[var] = value
        elif var in os.environ:
            del os.environ[var]


@pytest.fixture
def mock_env():
    """Fixture that sets up mock environment variables."""
    env_patch = patch.dict(
        os.environ,
        {
            "LLMAID_BASE_URL": "http://localhost:8080",
            "LLMAID_SECRET": "test-secret",
            "LLMAID_MODEL": "test-model",
            "LLMAID_STRICT_TEMPLATE": "true",
            "LLMAID_TEMPERATURE": "0.8",
            "LLMAID_MAX_TOKENS": "100",
        },
    )

    with env_patch:
        yield


@pytest.fixture
def basic_llmaid():
    """Fixture that provides a basic LLMAid instance for testing."""
    return llmaid.llmaid()


@pytest.fixture
def templated_llmaid():
    """Fixture that provides an LLMAid instance with a basic template."""
    return llmaid.llmaid().prompt_template(
        "You are a {{role}}, respond with {{response}}"
    )


@pytest.fixture
def temp_prompt_dir(tmp_path):
    """Fixture that creates a temporary directory with sample prompt files."""
    prompt_dir = tmp_path / "prompts"
    prompt_dir.mkdir()

    # Create sample prompt files
    (prompt_dir / "role.txt").write_text("You are a {{role}}")
    (prompt_dir / "task.txt").write_text("Your task is to {{task}}")
    (prompt_dir / "greeting.txt").write_text("Hello, {{name}}!")

    return prompt_dir


@pytest.fixture
def mock_completion_response():
    """Fixture that provides a standard completion response for mocking."""
    return {
        "choices": [
            {
                "text": "Test completion response"
            }
        ]
    }


@pytest.fixture
def mock_streaming_response():
    """Fixture that provides a standard streaming response for mocking."""
    return [
        b'data: {"choices":[{"text":"Hello"}]}\n\n',
        b'data: {"choices":[{"text":" world"}]}\n\n',
        b'data: {"choices":[{"text":"!"}]}\n\n',
        b'data: [DONE]\n\n'
    ]


@pytest.fixture
def completion_url():
    """Fixture that provides the completion endpoint URL."""
    return "http://127.0.0.1:17434/completions"


def mock_openai_api_completion(httpx_mock, response_text: str = "Test completion response"):
    """
    Helper to mock a standard OpenAI API completion response.
    
    Args:
        httpx_mock: The httpx mock fixture
        response_text: The text content to return in the response
    """
    httpx_mock.add_response(
        url="http://127.0.0.1:17434/completions",
        json={
            "choices": [
                {
                    "text": response_text
                }
            ]
        }
    )


def mock_openai_api_streaming(httpx_mock, tokens: List[str] = None):
    """
    Helper to mock a standard OpenAI API streaming response.
    
    Args:
        httpx_mock: The httpx mock fixture
        tokens: List of tokens to stream (defaults to ["Hello", " world", "!"])
    """
    if tokens is None:
        tokens = ["Hello", " world", "!"]
    
    stream_data = []
    for token in tokens:
        stream_data.append(f'data: {{"choices":[{{"text":"{token}"}}]}}\n\n'.encode())
    stream_data.append(b'data: [DONE]\n\n')
    
    httpx_mock.add_response(
        url="http://127.0.0.1:17434/completions",
        content=b''.join(stream_data),
        headers={"content-type": "text/plain"}
    )
