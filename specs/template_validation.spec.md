
## Feature: Template Validation

### 1. Scenario: Strict template with missing placeholders
    Given I have an llmaid instance with strict_template=True
    And a prompt template "Hello {{name}}, you are {{role}}"
    When I call completion with only name="John"
    Then a TemplateMismatchError should be raised
    And the error should indicate missing placeholder "role"
    And no backend call should be made

### 2. Scenario: Strict template with extra placeholders
    Given I have an llmaid instance with strict_template=True
    And a prompt template "Hello {{name}}"
    When I call completion with name="John" and extra="parameter"
    Then a TemplateMismatchError should be raised
    And the error should indicate unexpected placeholder "extra"
    And no backend call should be made

### 3. Scenario: Non-strict template with missing placeholders
    Given I have an llmaid instance with strict_template=False
    And a prompt template "Hello {{name}}, you are {{role}}"
    When I call completion with only name="John"
    Then the completion should succeed
    And "{{role}}" should remain unreplaced in the final prompt
    And no backend call should be made

### 4. Scenario: Non-strict template with extra placeholders
    Given I have an llmaid instance with strict_template=False
    And a prompt template "Hello {{name}}"
    When I call completion with name="John" and extra="parameter"
    Then the completion should succeed
    And the extra parameter should be ignored

### 5. Scenario: Happy path with all placeholders
    Given I have an llmaid instance with strict_template=True
    And a prompt template "Hello {{name}}, you are {{role}}"
    When I call completion with name="John" and role="Developer"
    Then the completion should succeed
    And the final prompt should be "Hello John, you are Developer"
    And the backend should receive the rendered prompt

### 6. Scenario: Template mismatch before backend call
    Given I have an llmaid instance with strict_template=True
    And a prompt template "Hello {{name}}"
    When I call completion with role="assistant" (wrong placeholder)
    Then a TemplateMismatchError should be raised
    And no backend call should be made

### 7. Scenario: Async completion with strict template validation
    Given I have an llmaid instance with strict_template=True
    And a prompt template "Hello {{name}}"
    When I call acompletion with role="assistant" (wrong placeholder)
    Then a TemplateMismatchError should be raised
    And no backend call should be made

### 8. Scenario: Async completion with valid placeholders
    Given I have an llmaid instance with strict_template=True
    And a prompt template "Hello {{name}}"
    When I call acompletion with name="Alice"
    Then the completion should succeed
    And the backend should receive the rendered prompt "Hello Alice"

### 9. Scenario: Streaming completion with strict template validation
    Given I have an llmaid instance with strict_template=True
    And a prompt template "Hello {{name}}"
    When I call stream with role="assistant" (wrong placeholder)
    Then a TemplateMismatchError should be raised
    And no backend call should be made

### 10. Scenario: Streaming completion with valid placeholders
    Given I have an llmaid instance with strict_template=True
    And a prompt template "Hello {{name}}"
    When I call stream with name="Bob"
    Then the streaming should succeed
    And the backend should receive the rendered prompt "Hello Bob"

---
