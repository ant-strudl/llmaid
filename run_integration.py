#!/usr/bin/env python3
"""
Integration test helper for LLMAid against real backends.

This is a standalone script for manually testing llmaid against real LLM providers.
Run this script to verify basic functionality before shipping.

Usage:
    python run_integration_test.py

The script will prompt you for:
- Backend URL
- Secret/API key  
- Model name

Then it will run through all basic completion methods and report results.
"""

import asyncio
import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from llmaid import llmaid
from llmaid.exceptions import ProviderError, ProviderHTTPError


def get_user_config():
    """Get backend configuration from user input."""
    print("🚀 LLMAid Integration Test Helper")
    print("=" * 50)
    print("This script will test llmaid against a real backend.")
    print("Please provide your backend configuration:\n")
    
    base_url = input("Backend URL (e.g., https://api.openai.com/v1): ").strip()
    if not base_url:
        print("❌ Backend URL is required")
        sys.exit(1)
    
    secret = input("API Secret/Key: ").strip()
    if not secret:
        print("❌ API secret is required")
        sys.exit(1)
    
    model = input("Model name (e.g., gpt-3.5-turbo, claude-3-sonnet): ").strip()
    if not model:
        print("❌ Model name is required")
        sys.exit(1)
    
    print("\n✅ Configuration:")
    print(f"   URL: {base_url}")
    print(f"   Secret: {'*' * (len(secret) - 4) + secret[-4:] if len(secret) > 4 else '***'}")
    print(f"   Model: {model}")
    
    confirm = input("\nProceed with testing? (y/N): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled by user")
        sys.exit(0)
    
    return {
        "base_url": base_url,
        "secret": secret,
        "model": model
    }


def test_basic_completion(config):
    """Test basic synchronous completion."""
    print("\n🔄 Testing basic completion...")
    
    try:
        instance = llmaid(**config)
        prompt = "Say hello in exactly 3 words."
        
        start_time = time.time()
        result = instance.completion(prompt)
        duration = time.time() - start_time
        
        print(f"✅ Basic completion successful ({duration:.2f}s)")
        print(f"   Prompt: {prompt}")
        print(f"   Response: {result[:100]}{'...' if len(result) > 100 else ''}")
        return True
        
    except Exception as e:
        print(f"❌ Basic completion failed: {e}")
        return False


def test_template_completion(config):
    """Test completion with prompt templating."""
    print("\n🔄 Testing template completion...")
    
    try:
        instance = llmaid(**config).prompt_template(
            "You are a {{role}}. Answer this question in exactly {{word_count}} words: {{question}}"
        )
        
        start_time = time.time()
        result = instance.completion(
            role="helpful assistant",
            word_count="5",
            question="What is the capital of France?"
        )
        duration = time.time() - start_time
        
        print(f"✅ Template completion successful ({duration:.2f}s)")
        print("   Template variables: role=helpful assistant, word_count=5, question=What is the capital of France?")
        print(f"   Response: {result[:100]}{'...' if len(result) > 100 else ''}")
        return True
        
    except Exception as e:
        print(f"❌ Template completion failed: {e}")
        return False


async def test_async_completion(config):
    """Test asynchronous completion."""
    print("\n🔄 Testing async completion...")
    
    try:
        instance = llmaid(**config)
        prompt = "What is 2+2? Answer with just the number."
        
        start_time = time.time()
        result = await instance.acompletion(prompt)
        duration = time.time() - start_time
        
        print(f"✅ Async completion successful ({duration:.2f}s)")
        print(f"   Prompt: {prompt}")
        print(f"   Response: {result[:100]}{'...' if len(result) > 100 else ''}")
        return True
        
    except Exception as e:
        print(f"❌ Async completion failed: {e}")
        return False


async def test_streaming_completion(config):
    """Test streaming completion."""
    print("\n🔄 Testing streaming completion...")
    
    try:
        instance = llmaid(**config)
        prompt = "Count from 1 to 3, each number on a new line."
        
        chunks = []
        start_time = time.time()
        
        print("   Streaming chunks: ", end="", flush=True)
        async for chunk in instance.stream(prompt):
            chunks.append(chunk)
            print(repr(chunk), end=" ", flush=True)
        
        duration = time.time() - start_time
        full_response = "".join(chunks)
        
        print(f"\n✅ Streaming completion successful ({duration:.2f}s)")
        print(f"   Prompt: {prompt}")
        print(f"   Chunks received: {len(chunks)}")
        print(f"   Full response: {full_response[:100]}{'...' if len(full_response) > 100 else ''}")
        return True
        
    except Exception as e:
        print(f"\n❌ Streaming completion failed: {e}")
        return False


def test_generation_params(config):
    """Test completion with generation parameters."""
    print("\n🔄 Testing completion with generation parameters...")
    
    try:
        instance = llmaid(
            **config,
            temperature=0.1,  # Low temperature for deterministic output
            max_tokens=30,    # Limit response length
        )
        
        prompt = "Explain quantum physics in simple terms."
        
        start_time = time.time()
        result = instance.completion(prompt)
        duration = time.time() - start_time
        
        print(f"✅ Generation params completion successful ({duration:.2f}s)")
        print(f"   Prompt: {prompt}")
        print("   Parameters: temperature=0.1, max_tokens=30")
        print(f"   Response: {result[:100]}{'...' if len(result) > 100 else ''}")
        return True
        
    except Exception as e:
        print(f"❌ Generation params completion failed: {e}")
        return False


def test_multiple_completions(config):
    """Test multiple completion requests."""
    print("\n🔄 Testing multiple completions...")
    
    try:
        instance = llmaid(**config)
        prompts = [
            "What color is the sky?",
            "What is 10 * 10?", 
            "Name one programming language."
        ]
        
        results = []
        for i, prompt in enumerate(prompts):
            start_time = time.time()
            result = instance.completion(prompt)
            duration = time.time() - start_time
            
            results.append(result)
            print(f"   Request {i+1} ({duration:.2f}s): {result[:50]}{'...' if len(result) > 50 else ''}")
        
        print(f"✅ Multiple completions successful ({len(results)} requests)")
        return True
        
    except Exception as e:
        print(f"❌ Multiple completions failed: {e}")
        return False


def test_error_handling(config):
    """Test error handling with invalid model."""
    print("\n🔄 Testing error handling...")
    
    try:
        # Use invalid model to trigger error
        bad_config = config.copy()
        bad_config["model"] = "definitely-not-a-real-model-name-12345"
        instance = llmaid(**bad_config)
        
        try:
            result = instance.completion("Hello world")
            print(f"❌ Error handling failed: Expected error but got response: {result}")
            return False
        except (ProviderError, ProviderHTTPError) as e:
            print(f"✅ Error handling successful: Correctly caught {type(e).__name__}: {e}")
            return True
        except Exception as e:
            print(f"❌ Error handling failed: Unexpected error type {type(e).__name__}: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False


async def run_all_tests(config):
    """Run all integration tests."""
    print("\n" + "=" * 50)
    print("🧪 Starting Integration Tests")
    print("=" * 50)
    
    tests = []
    
    # Sync tests
    tests.append(("Basic Completion", test_basic_completion(config)))
    tests.append(("Template Completion", test_template_completion(config)))
    tests.append(("Generation Parameters", test_generation_params(config)))
    tests.append(("Multiple Completions", test_multiple_completions(config)))
    tests.append(("Error Handling", test_error_handling(config)))
    
    # Async tests
    tests.append(("Async Completion", await test_async_completion(config)))
    tests.append(("Streaming Completion", await test_streaming_completion(config)))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! LLMAid is working correctly with your backend.")
    else:
        print("⚠️  Some tests failed. Check the configuration and backend status.")
    
    return passed == total


def main():
    """Main entry point."""
    try:
        config = get_user_config()
        success = asyncio.run(run_all_tests(config))
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
