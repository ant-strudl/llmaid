
## Feature: Error Handling and Retries

### 1. Scenario: HTTP 4XX error (non-retryable)
    Given I have an llmaid instance
    And I run a completion
    And the backend returns a 400 Bad Request error
    When I call completion
    Then a ProviderHTTPError should be raised
    And no retries should be attempted

### 2. Scenario: HTTP 429 rate limit error (retryable)
    Given I have an llmaid instance with max_retries=2
    And the backend returns 429 errors for the first 2 attempts
    And the backend returns success on the 3rd attempt
    When I call completion
    Then the completion should succeed after retries
    And exactly 3 attempts should be made

### 3. Scenario: Retry exhaustion
    Given I have an llmaid instance with max_retries=2
    And the backend always returns 429 errors
    When I call completion
    Then a RetryExhaustedError should be raised
    And exactly 3 attempts should be made (initial + 2 retries)

### 4. Scenario: Exponential backoff timing
    Given I have an llmaid instance with max_retries=3 and backoff_factor=1.0
    And the backend returns 500 errors for all attempts
    When I call completion
    Then the delays between attempts should be approximately 1s, 2s, 4s
    And a RetryExhaustedError should be raised

### 5. Scenario: Network timeout error
    Given I have an llmaid instance with max_timeout=1
    And I call completion
    And the answer is not completed within 1 second
    Then a ProviderTimeoutError should be raised

### 6. Scenario: Retryable server errors (500/503)
    Given I have an llmaid instance with max_retries=1
    And the backend returns a 500 error on first attempt
    And the backend returns success on second attempt
    When I call completion
    Then the completion should succeed after retry
    And exactly 2 attempts should be made

### 7. Scenario: Non-retryable client errors (401/403/404)
    Given I have an llmaid instance
    And the backend returns a 401/403/404 error
    When I call completion
    Then a ProviderHTTPError should be raised immediately
    And no retries should be attempted
