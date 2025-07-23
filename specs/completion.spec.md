
## Feature: Completion Methods

### 1. Scenario: Basic synchronous completion
    Given I have an llmaid instance with a prompt template "You are a {{role}}, respond with {{response}}"
    When I call completion with role="helper" and response="success"
    Then I should receive a string response
    And the backend should receive the rendered prompt

### 2. Scenario: Completion with positional arguments
    Given I have an llmaid instance with a prompt template "You are a helper"
    When I call completion("First question", "Second question")
    Then the final prompt should be "You are a helper\nFirst question\nSecond question"

### 3. Scenario: Completion with no arguments
    Given I have an llmaid instance with a prompt template "You are a helpful assistant. Respond with 'Hello!'"
    When I call completion with no arguments
    Then I should receive a string response
    And no additional text should be appended to the prompt

### 4. Scenario: Asynchronous completion
    Given I have an llmaid instance with a prompt template "You are a {{role}}"
    When I await acompletion with role="assistant"
    Then I should receive a string response asynchronously

### 5. Scenario: Streaming completion
    Given I have an llmaid instance with a prompt template "You are a {{role}}"
    When I iterate over stream with role="assistant"
    Then I should receive an async iterator yielding string tokens
    And each token should be a non-empty string

### 6. Scenario: Basic streaming iteration
    Given I have an llmaid instance
    When I iterate over stream("Hello")
    Then I should receive tokens as they arrive
    And each token should be a string
    And the concatenated tokens should form the complete response

### 7. Scenario: Streaming with template placeholders
    Given I have an llmaid instance with prompt template "You are {{role}}"
    When I iterate over stream with role="assistant"
    Then the stream should work with the rendered template

### 8. Scenario: Streaming cancellation
    Given I have an llmaid instance
    And I start iterating over stream("Long response")
    When I break out of the iteration early
    Then the HTTP connection should be closed
    And no further tokens should be received

### 9. Scenario: Streaming error handling
    Given I have an llmaid instance
    And the backend returns an error during streaming
    When I iterate over stream("Hello")
    Then the appropriate ProviderError should be raised

### 10. Scenario: Streaming backpressure
    Given I have an llmaid instance
    And the backend streams tokens slowly
    When I iterate over stream("Hello") with delays between iterations
    Then the stream should honor backpressure
    And tokens should arrive only when requested
