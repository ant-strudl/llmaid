## Feature: Prompt Template Security

### 1. Scenario: Oversized file rejection
    Given I have a text file larger than 64KB
    When I call prompt_template with the file path
    Then a ValueError should be raised indicating the file is too large
    And the error message should specify the maximum allowed size

### 2. Scenario: Invalid file extension rejection
    Given I have a file with an unsupported extension like ".py" or ".exe"
    When I call prompt_template with an explicit Path object pointing to that file
    Then a ValueError should be raised indicating the extension is not allowed
    And the error message should specify which extension was rejected

### 3. Scenario: Binary file content detection
    Given I have a file with a text extension but binary content (null bytes)
    When I call prompt_template with the file path
    Then a ValueError should be raised indicating the file appears to be binary
    And the file should not be loaded as a template

### 4. Scenario: Invalid UTF-8 encoding rejection
    Given I have a file with invalid UTF-8 byte sequences
    When I call prompt_template with the file path
    Then a ValueError should be raised indicating invalid encoding
    And the error message should specify UTF-8 validation failure

### 5. Scenario: Empty file prevention
    Given I have an empty text file
    When I call prompt_template with the file path
    Then a ValueError should be raised indicating the file is empty
    And the error message should explain this prevents developer confusion

### 6. Scenario: Unicode content support
    Given I have a text file with unicode characters (emojis, accents, non-Latin scripts)
    When I call prompt_template with the file path
    Then the unicode content should be properly decoded and included
    And the template should preserve all unicode characters

### 7. Scenario: String versus file path detection
    Given I have various string inputs with different characteristics
    When I call prompt_template with strings like "hello.world", "config.txt", "path/to/file"
    Then only strings that look like legitimate file paths should trigger file loading
    And strings without recognized extensions or path separators should be treated as literals

### 8. Scenario: Explicit Path object handling
    Given I pass a pathlib.Path object to prompt_template
    When the path exists and contains valid content
    Then it should always be treated as a file path regardless of extension
    And the file content should be loaded and validated

### 9. Scenario: Unsupported input type rejection
    Given I pass non-string, non-Path objects to prompt_template
    When I call prompt_template with integers, lists, dictionaries, or None
    Then a TypeError should be raised for each invalid type
    And the error message should specify the expected types

### 10. Scenario: File with no extension but text content
    Given I have a file with no extension containing valid text
    When I call prompt_template with an explicit Path object
    Then the file should be accepted based on content analysis
    And the text content should be loaded successfully

### 11. Scenario: Excessive control characters rejection
    Given I have a file with more than 10% control characters (excluding tab, LF, CR)
    When I call prompt_template with the file path
    Then a ValueError should be raised indicating excessive control characters
    And the file should be rejected as potentially binary

### 12. Scenario: MIME type validation
    Given I have files with various MIME types
    When I call prompt_template with each file
    Then only files with text-based MIME types should be accepted
    And files with binary MIME types should be rejected

### 13. Scenario: File size limit enforcement
    Given the system has a 64KB limit for template files
    When I attempt to load a file exceeding this limit
    Then the system should reject the file before reading its full content
    And provide a clear error message about the size limit

### 14. Scenario: Multiple validation layers
    Given a file must pass extension, size, MIME type, encoding, and content checks
    When any single validation fails
    Then the entire file loading should fail with a specific error
    And no partial content should be loaded or cached


### 16. Scenario: Developer-friendly error messages
    Given a file fails validation for any reason
    When the error is reported to the developer
    Then the error message should be specific and actionable
    And suggest how to fix the issue (file format, size, encoding, etc.)

### 17. Scenario: Allowed file extensions whitelist
    Given the system has a predefined list of safe extensions
    When I attempt to load files with various extensions
    Then only files with extensions in the whitelist should be processed
    And the whitelist should include: .txt, .md, .json, .yaml, .yml, .xml, .csv, .tsv, .template, .prompt, .tmpl

### 18. Scenario: Path traversal protection
    Given the system processes file paths from user input
    When file paths are resolved and validated
    Then the system should prevent access to unauthorized directories
    And restrict file access to designated template directories and current working directory

### 21. Scenario: String literal safety
    Given I provide template strings that are not file paths
    When I call prompt_template with content like "Hello {{name}}.txt"
    Then the string should be treated as a literal template
    And no file system access should be attempted


### 23. Scenario: File access error handling
    Given I specify a file path that exists but cannot be read (permissions, etc.)
    When I call prompt_template with that path
    Then a ValueError should be raised with file access details
    And the error should distinguish between "not found" and "cannot read"

### 24. Scenario: MIME type fallback detection
    Given I have a file with no extension or unknown extension
    When the MIME type cannot be determined from the extension
    Then the system should analyze file content to determine if it's text
    And make a conservative decision about file safety

### 25. Scenario: Control character tolerance
    Given I have a text file with some control characters like tabs and newlines
    When the control characters are within acceptable limits
    Then the file should be accepted as valid text
    And normal formatting characters should not trigger rejection
