# Developer Guide

This guide summarizes the main modules in the `lesson_generator` package to help you navigate and extend the codebase.

## Top-level layout

- `src/lesson_generator/cli/` — CLI entrypoints (Click)
  - `main.py` — `lesson-generator` command: argument parsing, environment load, progress UI
- `src/lesson_generator/core/` — Core orchestrator and utilities
  - `generator.py` — main orchestration: files/folders, templates, content generator, per-module pipeline
  - `file_manager.py` — filesystem helpers
  - `template_engine.py` — Jinja2 wrapper, template resolution
  - `topic_processor.py` — Pydantic models, parsing/normalization of topics
  - `template_extractor.py` — extract templates from a reference lesson
- `src/lesson_generator/content/` — Content generation backends
  - `__init__.py` — ContentGenerator protocol, FallbackContentGenerator (deterministic), caching wrapper
  - `openai_generator.py` — AI-backed generator (optional), retries and structured prompts
- `src/lesson_generator/templates/` — Built-in templates (Jinja2)
- `tests/` — Unit tests covering CLI, core, and content modules

## Data flow (high-level)

1. CLI collects topics (args or `--config`) and options (difficulty, modules, templates, cache, etc.)
2. `LessonGenerator` orchestrates:
   - Parse/normalize topics via `TopicProcessor`
   - Generate README, starter example, assignments, tests, extras using the content generator (AI or fallback)
   - Render templates and write package-like module directories
3. Tests are generated alongside code; starter smoke tests are created as well.

## Difficulty-aware generation

- `--difficulty` (or `-b/-i/-a`) sets `GenerationOptions.difficulty_override`
- Orchestrator propagates this to topic dicts and scales estimated times
- Content generators (AI and fallback) adjust method counts and small edge cases by difficulty

## Input normalization

- Topic/module names can be provided as free-form text
- `TopicModel` and `ModuleModel` validators convert names to lowercase snake_case internally
- Human-friendly titles are preserved in generated READMEs

## Extending the system

- Add new content methods by updating `ContentGenerator` protocol and both implementations
- Add templates to `src/lesson_generator/templates/` and reference them in `generator.py`
- Expose new options via `cli/main.py`; propagate options through `GenerationOptions`

## Quality gates

- Run `make coverage` to test and enforce 97%+ coverage
- Lint with `make lint`; typecheck with `make typecheck`

