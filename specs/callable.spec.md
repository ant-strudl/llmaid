
## Feature: Callable Clone Operator

### 1. Scenario: Basic parameter override
    Given I have an llmaid instance with model="original-model" and temperature=0.5
    When I call the instance with model="new-model"
    Then I should get a new llmaid instance
    And the new instance should have model "new-model"
    And the new instance should have temperature 0.5
    And the original instance should remain unchanged

### 2. Scenario: Multiple parameter override
    Given I have an llmaid instance with model="original" and temperature=0.5
    When I call the instance with model="new", temperature=0.8, max_tokens=100
    Then the new instance should have all the new parameters
    And the original instance should remain unchanged

### 3. Scenario: Generation knob override
    Given I have an llmaid instance with temperature=0.2
    When I call the instance with temperature=0.9, top_p=0.8
    Then the new instance should have temperature 0.9
    And the new instance should have top_p 0.8

### 4. Scenario: Model parameter override
    Given I have an llmaid instance with model_parameter={"param1": "value1"}
    When I call the instance with model_parameter={"param2": "value2"}
    Then the new instance should have model_parameter {"param2": "value2"}

### 5. Scenario: Invalid parameter in clone
    Given I have an llmaid instance
    When I call the instance with invalid_parameter="value"
    Then a ConfigurationError should be raised

### 6. Scenario: Mixed valid and invalid parameters
    Given I have an llmaid instance with model="test-model"
    When I call the instance with temperature=0.8, invalid_param="value", another_invalid="test"
    Then a ConfigurationError should be raised
    And the error message should contain the invalid parameter names

### 7. Scenario: No parameters clone
    Given I have an llmaid instance with model="test-model" and temperature=0.7
    When I call the instance with no parameters
    Then I should get a new llmaid instance
    And the new instance should have identical configuration
    And the instances should be different objects

### 8. Scenario: Clone preserves all settings
    Given I have an llmaid instance with multiple configuration parameters
    When I call the instance overriding only a few parameters
    Then the new instance should have the overridden values
    And all other parameters should be preserved from the original

### 9. Scenario: Clone with prompt template
    Given I have an llmaid instance with a prompt template
    When I call the instance with model override
    Then the new instance should preserve the prompt template
    And the new instance should have the overridden model

### 10. Scenario: Chained cloning
    Given I have a base llmaid instance
    When I create multiple sequential clones with different overrides
    Then each clone should inherit from its immediate parent
    And each clone should be independent of others
    And the base instance should remain unchanged

