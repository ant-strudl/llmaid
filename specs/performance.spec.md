## Feature: Performance and Concurrency

### 1. Scenario: Multiple concurrent completions
    Given I have an llmaid instance
    When I make 5 concurrent async completion calls
    Then all completions should succeed
    And each should receive independent responses

### 2. Scenario: Concurrent streaming
    Given I have an llmaid instance
    When I start multiple concurrent streams
    Then each stream should work independently
    And tokens should not be mixed between streams

### 3. Scenario: Instance sharing between threads
    Given I have an llmaid instance
    When I use the same instance from multiple threads
    Then the instance should be thread-safe
    And all operations should work correctly

### 6. Scenario: Connection cleanup
    Given I have an llmaid instance
    When I make multiple completion calls
    And I cancel them all
    Then HTTP connections should be properly closed