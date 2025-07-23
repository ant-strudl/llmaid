#!/usr/bin/env python3
"""
Test runner script for LLMAid.

This script provides convenient ways to run tests with different configurations.
"""

import subprocess
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent


def run_command(cmd, description=""):
    """Run a command and return the result."""
    if description:
        print(f"\n🔄 {description}")
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    
    if result.returncode == 0:
        print(f"✅ {description or 'Command'} completed successfully")
    else:
        print(f"❌ {description or 'Command'} failed with exit code {result.returncode}")
    
    return result.returncode


def run_tests():
    """Run the main test suite."""
    return run_command([
        str(PROJECT_ROOT / ".venv" / "bin" / "python"),
        "-m", "pytest", 
        "tests/",
        "-v",
        "--tb=short"
    ], "Running test suite")

def run_lint():
    """Run linting with flake8."""
    return run_command([
        str(PROJECT_ROOT / ".venv" / "bin" / "flake8"),
        "src/",
        "tests/",
        "--max-line-length=88",
        "--extend-ignore=E203,W503"
    ], "Running linter")


def run_format():
    """Format code with black."""
    return run_command([
        str(PROJECT_ROOT / ".venv" / "bin" / "black"),
        "src/",
        "tests/"
    ], "Formatting code")


def run_type_check():
    """Run type checking with mypy."""
    return run_command([
        str(PROJECT_ROOT / ".venv" / "bin" / "mypy"),
        "src/llmaid/"
    ], "Running type checker")


def run_all():
    """Run all checks: format, lint, type check, and tests."""
    results = []
    
    results.append(run_format())
    results.append(run_lint())
    results.append(run_type_check())
    results.append(run_tests())
    
    failed = sum(1 for r in results if r != 0)
    if failed == 0:
        print("\n🎉 All checks passed!")
        return 0
    else:
        print(f"\n💥 {failed} check(s) failed!")
        return 1


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python run_tests.py <command>")
        print("\nAvailable commands:")
        print("  test       - Run all tests")
        print("  lint       - Run linter")
        print("  format     - Format code")
        print("  typecheck  - Run type checker")
        print("  all        - Run format, lint, typecheck, and tests")
        return 1
    
    command = sys.argv[1].lower()
    
    if command == "test":
        return run_tests()
    elif command == "lint":
        return run_lint()
    elif command == "format":
        return run_format()
    elif command == "typecheck":
        return run_type_check()
    elif command == "all":
        return run_all()
    else:
        print(f"Unknown command: {command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
