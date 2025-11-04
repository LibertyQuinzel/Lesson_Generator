# Lesson Generator - User Guide

## Overview
Generate course lessons from topics using built-in templates and optional AI. Supports multiple topics, parallel generation, and custom templates.

## Installation
- Create a virtual environment and install editable:
  - `pip install -e .` from the `lesson_generator/` folder
- Or use the Makefile targets in generated lessons for quality checks.

## CLI
```
Usage: lesson-generator create [OPTIONS] [TOPICS]...

Options:
  --config PATH                    Path to a JSON file with topic definitions
  --output DIRECTORY               Output directory (default: generated_lessons)
  --modules INTEGER                Override number of modules per lesson
  --dry-run                        Show plan only; don’t write files
  --openai-api-key TEXT            OpenAI API key
  --no-ai                          Disable OpenAI; deterministic content
  --workers INTEGER RANGE          Parallel workers for multiple topics
  --templates DIRECTORY            Custom templates directory
  --difficulty [beginner|intermediate|advanced]
                                   Override difficulty for all topics
  -b | -i | -a                     Shortcuts for beginner | intermediate | advanced difficulty
  --cache / --no-cache             Enable/disable caching of content generation
  -h, --help                       Show this message and exit
```

### Examples
- Generate a single lesson by topic name:
  - `lesson-generator create async_programming`
- Generate multiple lessons in parallel:
  - `lesson-generator create async_programming design_patterns --workers 4`
- Use a JSON config with topics array:
  - `lesson-generator create --config topics.json --workers 4`
- Use custom templates:
  - `lesson-generator create async_programming --templates ./my_templates`
- Override difficulty globally:
  - `lesson-generator create async_programming --difficulty advanced`
- Disable AI and use cache:
  - `lesson-generator create async_programming --no-ai --cache`

## Templates
- Built-in templates live in `src/lesson_generator/templates`.
- Provide a directory with files of the same names to override.
- Jinja autoescape is disabled to preserve Python code; guard inputs accordingly.
 - Precedence when multiple sources exist: `--templates` directory > templates extracted via `--reference` > built-ins.

## Caching
- `--cache/--no-cache` toggles a lightweight generation cache (enabled by default).
- When on, identical generation requests within the same run reuse previously produced content instead of re-calling AI/fallback generators.
- Useful for iterative runs, multiple topics, or when tweaking non-content options.
- The cache is in-memory for the current process only and is not persisted to disk.

## Difficulty Scaling
- Estimated times adjust based on `--difficulty`:
  - Beginner: ~20% lower
  - Intermediate: baseline
  - Advanced: ~30% higher
- Code complexity also scales with difficulty (within tight bounds to keep lessons approachable):
  - Starter examples: beginner includes 1–2 simple methods; advanced may include 3–4 small methods with a minor edge case.
  - Assignments: beginner has 1–2 straightforward public methods; advanced adds 1–2 small methods (e.g., count, sum_positive) while keeping deterministic behavior.
  - Tests remain concise; advanced may include slightly broader coverage when AI is enabled.

## Input Sanitation
- Topic and module names can be provided as plain text (no need to supply snake_case). The generator normalizes names to lowercase snake_case internally while keeping human-friendly titles in README files.

## Generated Structure
- Root: `README.md`, `requirements.txt`, `pytest.ini`, `Makefile`, `setup.cfg`
- Modules: `README.md`, `starter_example.py`, `assignment_a.py`, `test_assignment_a.py`,
  optionally `assignment_b.py` + tests, `extra_exercises.md`, `test_starter_example.py`

## Troubleshooting
- If AI fails or returns invalid JSON, the system falls back to deterministic content.
- For multiple topics, use `--workers` to speed up generation.
- Use the generated Makefile for formatting, linting, type-checking, and tests.

## Performance and Benchmarking

For quick performance checks and to compare parallel worker settings, see `docs/PERFORMANCE.md`.

Quick start:

- From the `lesson_generator/` folder, run the helper script:
  - `python scripts/benchmark_generation.py --topics 20 --workers 1 2 4 8 --output /tmp/bench_out`

The script uses the deterministic content generator (no network calls) and prints a single line per run with topic count, worker count, duration, and success ratio.
