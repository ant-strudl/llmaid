## Feature: Client Base URL Handling

### 1. Scenario: Standard OpenRouter base URL with /api/v1
    Given I create an llmaid client with base_url="https://openrouter.ai/api/v1"
    When I make a completion request
    Then the HTTP request should be sent to "https://openrouter.ai/api/v1/completions"
    And the request should succeed

### 2. Scenario: OpenRouter base URL with /api/ trailing slash
    Given I create an llmaid client with base_url="https://openrouter.ai/api/"
    When I make a completion request
    Then the HTTP request should be sent to "https://openrouter.ai/api/completions"
    And the request should succeed

### 3. Scenario: OpenRouter base URL with root / trailing slash
    Given I create an llmaid client with base_url="https://openrouter.ai/"
    When I make a completion request
    Then the HTTP request should be sent to "https://openrouter.ai/completions"
    And the request should succeed

### 4. Scenario: OpenRouter base URL without trailing slash
    Given I create an llmaid client with base_url="https://openrouter.ai"
    When I make a completion request
    Then the HTTP request should be sent to "https://openrouter.ai/completions"
    And the request should succeed

### 5. Scenario: Standard OpenRouter base URL with /api/v1/ trailing slash
    Given I create an llmaid client with base_url="https://openrouter.ai/api/v1/"
    When I make a completion request
    Then the HTTP request should be sent to "https://openrouter.ai/api/v1/completions"
    And the request should succeed

### 6. Scenario: OpenAI-style base URL
    Given I create an llmaid client with base_url="https://api.openai.com/v1"
    When I make a completion request
    Then the HTTP request should be sent to "https://api.openai.com/v1/completions"
    And the request should succeed

### 7. Scenario: Custom provider base URL normalization
    Given I create an llmaid client with base_url="https://custom-provider.com/api/v2/"
    When I make a completion request
    Then the HTTP request should be sent to "https://custom-provider.com/api/v2/completions"
    And the request should succeed

### 8. Scenario: Base URL trailing slash handling
    Given I create an llmaid client with any base_url ending with "/"
    When the client normalizes the base URL
    Then the trailing slash should be removed before appending endpoints
    And the final URL should not contain double slashes