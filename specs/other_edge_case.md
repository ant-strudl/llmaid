## Feature: Other Edge Cases

### 1. Scenario: Unicode in prompt templates
    Given I have a prompt template "Translate to français: {{text}}"
    When I call completion with text="Hello world"
    Then the unicode characters should be preserved
    And the completion should work correctly

### 2. Scenario: Unicode in completion responses
    Given I have an llmaid instance
    When the backend returns unicode characters in the response
    Then the unicode should be preserved in the returned string

### 3. Scenario: Special characters in placeholders
    Given I have a prompt template with "{{user_input}}"
    When I call completion with user_input containing quotes and newlines
    Then the special characters should be properly handled

### 4. Scenario: Special characters and asian languages
    Given I have a prompt template "Translate to 中文: {{text}}"
    When I call completion with text="Hello 世界"
    Then the special characters should be preserved
    And the completion should return the correct translation

### 5. Scenario: Empty prompt template
    Given I have an llmaid instance
    When I call prompt_template("")
    Then I should get a new instance with empty template
    And completion should work with just positional arguments

### 6. Scenario: Empty completion input
    Given I have an llmaid instance with a prompt template "Respond with 'OK'"
    When I call completion() with no arguments
    Then the completion should work with just the template

### 7. Scenario: Strict Large prompt template
    Given I have a very large prompt template that exceeds max context length (9000 tokens)
    And strict_context_length is set to True
    And context_length is set to 8192
    When I call completion
    Then llmaid should raise a ContextLengthExceededError

### 8. Scenario: Large prompt template
    Given I have a very large prompt template that exceeds max context length (9000 tokens)
    And strict_context_length is set to False
    And context_length is set to 8192
    When I call completion
    Then llmaid should perform as usual and send the full context to provider.
    And llmaid should log a warning context length being too large.

### 9. Scenario: Many placeholders
    Given I have a prompt template with 50 different placeholders
    When I call completion with all 50 placeholders filled
    Then all placeholders should be correctly replaced
