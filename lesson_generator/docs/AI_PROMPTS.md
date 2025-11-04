# AI Prompts and Content Contracts

This document describes how we prompt the AI and the expected JSON contracts for each content type. These contracts power our templates and are validated minimally at generation time.

## Models and Settings
- Provider: OpenAI Chat Completions
- Default model: `gpt-4o-mini`
- Temperature: 0.7 (balanced creativity)
- Retries: exponential backoff (up to 3 attempts via tenacity)
- Fallback: Deterministic content when API errors occur

## Learning Path Prompt
System: "You are an expert educator generating concise, structured module content."

User content includes:
- Topic title
- Module title
- Focus areas (comma-separated)

Expected JSON keys:
- `introduction`: string
- `concepts`: object keyed by focus area name
  - `philosophy`: string
  - `example_code`: string (Python)
  - `use_cases`: string[]
  - `advantages`: string[]
- `practical_examples`: array
  - `title`: string
  - `description`: string
  - `code`: string (Python)
  - `key_points`: string[]
- `testing_areas`: string[]
- `advanced_concepts`: array
  - `title`: string
  - `description`: string
  - `example`: string (Python)

## Starter Example Prompt
System: "You generate small, runnable Python starter examples for a module."

Expected JSON keys:
- `title`, `description`, `learning_objectives[]`, `detailed_explanation`
- `imports[]`: e.g., `from typing import Any`
- `class_name`, `class_description`, `concepts[]`
- `methods[]` entries with:
  - `name`, `parameters` (e.g., ", x: int = 0"), `docstring`
  - `demonstrates`, `args[]` (name, type, description)
  - `return_type`, `return_description`
  - `example_usage`, `example_output`, `explanation`, `implementation`
- `demonstrations[]`: with `function_call` (ready-to-run expression, e.g., `print("Demo", Foo().bar())`)

## Assignment Prompt
System: "You generate small Python assignments with docstrings and examples."

Expected JSON keys:
- `title`, `description`, `imports[]`, `class_name`, `class_description`, `learning_focus`
- `methods[]`: similar to Starter, with optional `examples[]` (usage, expected_output)
- `helper_functions[]`
- `examples[]` (description, code)

## Tests for Assignment Prompt
System: "You generate pytest tests for a given assignment context."

Expected JSON keys:
- `test_target_name`, `test_target_description`, `test_imports[]`
- `module_path`, `class_name`
- `test_coverage_areas[]`
- `fixtures[]`
- `test_methods[]` (name, description, tests, given_section, when_section, then_section)
- `parametrized_tests[]`, `error_tests[]`, `integration_tests[]`, `performance_tests[]`, `test_utilities[]`

## Validation & Safety
- We parse JSON strictly and fallback to deterministic content if parsing or API calls fail.
- We perform basic syntax validation (`compile()`) on generated Python files before writing.
- Jinja autoescape is disabled to preserve Python code; templates must ensure safe insertion.
- Optional list-like fields are guarded in templates using `or []` to prevent iteration over `None`.

## Examples
See unit tests under `tests/unit/test_content/test_openai_generator.py` for minimal examples and behaviors (success and fallback).
