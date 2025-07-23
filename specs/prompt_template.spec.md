
## Feature: Prompt Template Management

### 1. Scenario: Basic inline prompt template
    Given I have an llmaid instance
    When I call prompt_template("You are a {{role}} machine, only say {{action}}!")
    Then I should get a new llmaid instance
    And the new instance should have the prompt template "You are a {{role}} machine, only say {{action}}!"

### 2. Scenario: Multiple inline templates concatenation
    Given I have an llmaid instance
    When I call prompt_template("First part", "Second part", "Third part")
    Then I should get a new llmaid instance
    And the new instance should have the prompt template "First part\n\nSecond part\n\nThird part"

### 3. Scenario: File-based prompt template
    Given I have a file "test_prompt.txt" containing "You are a helpful {{role}}"
    And I have an llmaid instance with prompt_template_dir="./prompts"
    When I call prompt_template("test_prompt.txt")
    Then I should get a new llmaid instance
    And the new instance should have its prompt template set to the file content "You are a helpful {{role}}"

### 4. Scenario: Mixed inline and file templates
    Given I have a file "role.txt" containing "You are a {{role}}"
    And I have an llmaid instance with prompt_template_dir="./prompts"
    When I call prompt_template("role.txt", "Additional instructions: {{instructions}}")
    Then I should get a new llmaid instance
    And the templates should be concatenated with two newlines

### 5. Scenario: System prompt alias
    Given I have an llmaid instance
    When I call system_prompt("You are a {{role}} assistant")
    Then I should get a new llmaid instance
    And the behavior should be identical to calling prompt_template

### 6. Scenario: Strict template override
    Given I have an llmaid instance with strict_template=True
    When I call prompt_template("Hello {{name}}", strict_template=False)
    Then the new instance should have strict_template False

### 7. Scenario: Absolute path template loading
    Given I have a file at "/absolute/path/prompt.txt" containing "Hello {{name}}"
    When I call prompt_template("/absolute/path/prompt.txt")
    Then the file should be loaded directly without using prompt_template_dir

### 8. Scenario: Relative path fallback to current directory
    Given I have an llmaid instance with no prompt_template_dir set
    And I have a file "local_prompt.txt" in the current directory
    When I call prompt_template("local_prompt.txt")
    Then the file should be loaded from the current directory

### 9. Scenario: Multiple file concatenation
    Given I have files "part1.txt" and "part2.txt" in prompt directory
    And "part1.txt" contains "You are a {{role}}"
    And "part2.txt" contains "Task: {{task}}"
    When I call prompt_template("part1.txt", "part2.txt")
    Then the resulting template should be "You are a {{role}}\n\nTask: {{task}}"

### 10. Scenario: Mixed file and inline templates
    Given I have file "role.txt" containing "You are a {{role}}"
    When I call prompt_template("role.txt", "Additional: {{note}}")
    Then the file content and inline text should be concatenated

### 11. Scenario: Nested directory template loading
    Given I have "prompts/roles/scientist.txt" containing "You are a scientist"
    And prompt_template_dir is set to "prompts"
    When I call prompt_template("roles/scientist.txt")
    Then the file should be loaded successfully

### 12. Scenario: Template file not found
    Given prompt_template_dir is set to "prompts"
    And "nonexistent.txt" does not exist
    When I call prompt_template("nonexistent.txt")
    Then a FileNotFoundError should be raised

### 13. Scenario: Chat history through templating
    Given I have a prompt template with {{chat_history}} and {{user_input}} placeholders
    And I have existing chat history "User: Hi\nAssistant: Hello"
    When I call completion with chat_history="User: Hi\nAssistant: Hello" and user_input="How are you?"
    Then the template should be rendered with both parameters
    And the completion should consider the chat context