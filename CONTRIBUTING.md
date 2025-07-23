This contributing guide outlines the steps to follow when contributing to the LLMAid project.

## Contributing Process

Human tasks:
1. Think harder about the next feature you want to add, or the next bug you want to fix.
2. Brainstorm, and visualize how it should look like, and how it should behave, as clearly and precisely as you can.
- for a feature,
    - explain how the feature should behave in your mind
    - write an example code snippet that illustrates the feature in a new section of the [README.md](README.md)
    - then create test relevant scenarios in the `specs` directory. Add new scenarios to existing files for feature extensions, or create a new file for a new feature.
- for a bug
    - explain the scenario that causes the bug in your mind
    - explain how it should behave instead
    - write a test scenario that would fail because of the bug according to how it should behave

AI tasks:
3. Based on the new or changed test scenarios in the `specs` directory (think git diffs), Have AI add or modify existing test scenarios and cases in the `tests` directory.
4. Based on the new or changed test scenarios in the `tests` directory, implement the feature or fix the bug in the `src` directory.
5. Run the tests to ensure everything works as expected. If not, go back to previous step and iterate until all tests pass.


## Project Structure

- `CONTRIBUTING.md`: This file, outlining the contribution process.
- `README.md`: The main documentation file, providing an overview and quick start guide.
- `docs/Public API Reference.md`: A detailed and exhaustive API reference for LLMAid, including all public methods and their usage. It is the ground truth and authoritative source for the library's API and specs.
- `specs/`: Contains Gherkin-style test specifications of all the features and behaviors documented in the full API reference. It is the authoritative source for the expected behavior of the LLMAid library.
- `tests/`: Contains the actual test implementations that validate the behaviors described in the specs. It features a Pytest test suite, and a mock llm backend for testing purposes.
- `src/`: Contains the source code of the LLMAid library, including the main functionality and API implementations.
- `LICENSE.md`: The license file for the project.