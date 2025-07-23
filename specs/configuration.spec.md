
## Feature: Configuration and Instantiation

### 1. Scenario: Default instantiation with environment variables
    Given the environment variable LLMAID_BASE_URL is set to "http://localhost:8080"
    And the environment variable LLMAID_SECRET is set to "test-secret"
    And the environment variable LLMAID_MODEL is set to "test-model"
    When I create an llmaid instance with no parameters
    Then the instance should have base_url "http://localhost:8080"
    And the instance should have secret "test-secret"
    And the instance should have model "test-model"

### 2. Scenario: Constructor parameter overrides environment variables
    Given the environment variable LLMAID_BASE_URL is set to "http://localhost:8080"
    And the environment variable LLMAID_MODEL is set to "env-model"
    When I create an llmaid instance with base_url="http://custom:9000" and model="custom-model"
    Then the instance should have base_url "http://custom:9000"
    And the instance should have model "custom-model"

### 3. Scenario: Default values when no environment variables are set
    Given no LLMAID environment variables are set
    When I create an llmaid instance with no parameters
    Then the instance should have base_url "http://127.0.0.1:17434"
    And the instance should have secret None
    And the instance should have model "mistral-large-v0.1"
    And the instance should have prompt_template_dir None
    And the instance should have strict_template True

### 4. Scenario: Generation parameters configuration
    Given no environment variables are set
    When I create an llmaid instance with temperature=0.8, max_tokens=100, top_p=0.9
    Then the instance should have temperature 0.8
    And the instance should have max_tokens 100
    And the instance should have top_p 0.9

### 5. Scenario: Model parameters configuration
    Given no environment variables are set
    When I create an llmaid instance with model_parameter={"custom_param": "value"}
    Then the instance should have model_parameter containing {"custom_param": "value"}

### 6. Scenario: Environment variable type conversion
    Given the environment variable LLMAID_STRICT_TEMPLATE is set to "false"
    And the environment variable LLMAID_TEMPERATURE is set to "0.7"
    And the environment variable LLMAID_MAX_TOKENS is set to "200"
    When I create an llmaid instance with no parameters
    Then the instance should have strict_template False
    And the instance should have temperature 0.7
    And the instance should have max_tokens 200

---
