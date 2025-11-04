"""OpenAI-powered content generator with retries and graceful fallbacks."""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

try:  # Optional import to allow tests without OpenAI
    from openai import OpenAI
except Exception:  # pragma: no cover - import guard for environments without package
    OpenAI = None  # type: ignore


class OpenAIContentGenerator:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini", allow_fallbacks: bool = True) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.model = model
        self.allow_fallbacks = allow_fallbacks
        self._client = None
        if self.api_key and OpenAI is not None:
            self._client = OpenAI(api_key=self.api_key)

    # Generic safe call wrapper
    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=0.5, max=4),
        retry=retry_if_exception_type(Exception),
    )
    def _complete(self, system: str, prompt: str, temperature: float = 0.7) -> str:
        if not self._client:
            raise RuntimeError("OpenAI client not initialized")
        # Prefer JSON mode to increase structured response reliability; if not supported, fall back.
        try:
            resp = self._client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            )
        except Exception:
            resp = self._client.chat.completions.create(
                model=self.model,
                temperature=temperature,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": prompt}],
            )
        return resp.choices[0].message.content or ""

    # Public API expected by the templates/orchestrator
    def learning_path(self, topic: dict, module: dict) -> Dict[str, Any]:
        system = (
            "You are an expert educator generating tightly structured module content. "
            "Style: crisp, to-the-point sentences; avoid filler and repetition. "
            "Prioritize clarity and brevity while remaining complete. Output must be valid JSON only."
        )
        prompt = f"""
        Topic: {topic['title']}
        Module: {module['title']}
        Focus areas: {', '.join(module.get('focus_areas', []))}

        Produce JSON with keys: introduction, concepts (object keyed by focus name with philosophy, example_code, use_cases[], advantages[]), practical_examples (title, description, code, key_points[]), testing_areas[], advanced_concepts[] (title, description, example).
        Keep code Pythonic. Respond with JSON only.
        """
        try:
            import json

            raw = self._complete(system, prompt)
            return json.loads(raw)
        except Exception:
            # Optional fallback
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator

            return FallbackContentGenerator().learning_path(topic, module)

    def starter_example(self, topic: dict, module: dict) -> Dict[str, Any]:
        system = (
            "You generate fully implemented, runnable Python starter examples that showcase the module's topic (not tests). "
            "These are NOT smoke tests; they should provide a small but meaningful API (1–3 methods) that demonstrates the concept. "
            "Constraints: deterministic behavior, no external dependencies, no network/file I/O, PEP 8 friendly. "
            "Include a trivial demo() method returning 'ok' to support a separate smoke test file. "
            "Style: concise and direct. Output must be valid JSON only. "
            "Critically, when a module learning_path.md reference is provided, align the starter's focus, class_name, methods, and examples to that reference. "
            "Do not contradict the reference; prefer its terminology."
        )
        lp_md = module.get("learning_path_md", "")
        difficulty = (topic.get("difficulty") or "intermediate").lower()
        lp_note = "Learning path reference provided below. Use it to match concepts and objectives." if lp_md else "No learning path reference provided. Use topic/module fields only."
        prompt = f"""
        Topic: {topic['title']}, Module: {module['title']}
        {lp_note}

        Reference - learning_path.md:
        ---
        {lp_md}
        ---

        Difficulty: {difficulty}
        Adjust API complexity by difficulty: beginner = 1-2 very simple public methods; intermediate = 2-3 methods of moderate complexity; advanced = 3-4 methods and include at least one small edge-case handling path. Keep deterministic behavior.

        Provide JSON matching keys: title, description, learning_objectives[], detailed_explanation, imports[], class_name, class_description, concepts[], methods[] (name, parameters, docstring, demonstrates, args[], return_type, return_description, example_usage, example_output, explanation, implementation), demonstrations[] (function_call).
        Keep implementations short and runnable. Ensure titles, concepts, and examples are consistent with the learning path when available. JSON only.
        """
        try:
            import json

            raw = self._complete(system, prompt)
            return json.loads(raw)
        except Exception:
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator

            return FallbackContentGenerator().starter_example(topic, module)

    # Direct code variant: return a complete Python file as str
    def starter_example_code(self, topic: dict, module: dict) -> str:
        system = (
            "You generate complete, runnable starter_example.py files that fully implement a small example API for the module's topic. "
            "These files are not tests; they should demonstrate the concept with 1–3 meaningful, deterministic methods. "
            "Constraints: single module file, safe imports only (typing, dataclasses, math, functools), no I/O, no network, no exec/eval, no subprocess. "
            "Also include a trivial demo() method that returns 'ok' to enable a separate minimal smoke test. "
            "Provide ONLY raw Python code, no Markdown fences."
        )
        lp_md = module.get("learning_path_md", "")
        lp_note = (
            "A learning_path.md reference is provided below. Align class name, methods and examples with it."
            if lp_md
            else "No learning path reference provided. Base on topic/module."
        )
        prompt = f"""
        Topic: {topic['title']}
        Module: {module['title']}
        {lp_note}

    Produce a single Python file that defines one main class with a short docstring and 1–3 topic-focused methods, plus a demo() method returning 'ok'.
    Keep code PEP 8 friendly and minimal, but fully implemented to illustrate the concept. Avoid forbidden imports (os, subprocess, shlex, socket, requests).

        Reference - learning_path.md:
        ---
        {lp_md}
        ---

        Output: ONLY the Python code for the file, no backticks.
        """
        try:
            return self._complete(system, prompt, temperature=0.4)
        except Exception:
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator

            ctx = FallbackContentGenerator().starter_example(topic, module)
            from lesson_generator.core.template_engine import TemplateEngine  # local import to avoid cycles
            # Render using built-in template as a fallback path
            eng = TemplateEngine(None)
            return eng.render("starter_example.py.j2", {"example": ctx})

    def assignment(self, topic: dict, module: dict, variant: str = "a") -> Dict[str, Any]:
        system = (
            "You generate small Python assignments with clear docstrings and minimal examples. "
            "Keep APIs simple, deterministic, and testable. No external deps, no I/O. "
            "Hard limit: include no more than 4 public methods/functions in total. "
            "Style: concise, no fluff. Output must be valid JSON only. "
            "When a learning_path.md reference is available, ensure the assignment aligns with its concepts, focus areas, and objectives."
        )
        lp_md = module.get("learning_path_md", "")
        difficulty = (topic.get("difficulty") or "intermediate").lower()
        lp_note = "Learning path reference provided below. Match the assignment's API and examples to it." if lp_md else "No learning path reference provided. Base the assignment on the module fields."
        prompt = f"""
        Topic: {topic['title']}, Module: {module['title']}, Variant: {variant}
        {lp_note}

        Reference - learning_path.md:
        ---
        {lp_md}
        ---

    Difficulty: {difficulty}
    Adjust complexity by difficulty:
    - beginner: 1-2 simple public methods with straightforward logic and examples
    - intermediate: 2-3 methods with minor branching and 1-2 edge-case examples
    - advanced: 3-4 methods; include small edge-case paths and slightly richer input types where still deterministic

    Provide JSON for keys: title, description, imports[], class_name, class_description, learning_focus, methods[] (name, parameters, docstring, args[], return_type, return_description, examples[] (usage, expected_output), implementation), helper_functions[], examples[] (description, code).
        Keep simple and testable. Ensure naming and behaviors reflect the referenced learning path where provided. JSON only.
        """
        try:
            import json

            raw = self._complete(system, prompt)
            return json.loads(raw)
        except Exception:
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator

            return FallbackContentGenerator().assignment(topic, module, variant)

    # Direct code variant for assignments
    def assignment_code(self, topic: dict, module: dict, variant: str = "a") -> str:
        system = (
            "You generate Python assignment files. "
            "Constraints: one main class with 2-4 small public methods, deterministic, no I/O/network, "
            "safe imports only (typing, dataclasses), PEP 8, short docstrings. "
            "Variant-specific rules: For variant 'a', produce a complete, working implementation. "
            "For variant 'b', produce a skeleton suitable for TDD where core methods raise NotImplementedError and "
            "docstrings/examples describe the required behavior. "
            "Provide ONLY raw Python code, no Markdown fences."
        )
        lp_md = module.get("learning_path_md", "")
        difficulty = (topic.get("difficulty") or "intermediate").lower()
        lp_note = (
            "Use the learning_path.md reference to align APIs and example behaviors."
            if lp_md
            else "No learning path reference provided. Base on topic/module."
        )
        prompt = f"""
        Topic: {topic['title']}, Module: {module['title']}, Variant: {variant}
        {lp_note}

        Produce a single Python file with:
        - one main class named to reflect the module
        - public methods with clear type hints and docstrings (difficulty-driven count): beginner=1-2, intermediate=2-3, advanced=3-4
        - simple examples as comments (no code fences) inside the file
        - Variant A: include working implementations
        - Variant B: leave core logic unimplemented (raise NotImplementedError) while keeping clear docstrings
        Avoid forbidden imports (os, subprocess, shlex, socket, requests).

        Reference - learning_path.md:
        ---
        {lp_md}
        ---

        Difficulty: {difficulty} (use this to calibrate method count and minor complexity only; keep deterministic and beginner-friendly naming.)

        Output: ONLY the Python code for the file, no backticks.
        """
        try:
            return self._complete(system, prompt, temperature=0.4)
        except Exception:
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator

            ctx = FallbackContentGenerator().assignment(topic, module, variant)
            from lesson_generator.core.template_engine import TemplateEngine  # local import
            eng = TemplateEngine(None)
            return eng.render("assignment.py.j2", ctx)

    def tests_for_assignment(self, topic: dict, module: dict, assignment_ctx: Dict[str, Any]) -> Dict[str, Any]:
        system = (
            "You generate focused pytest tests for a given assignment. "
            "You WILL be provided the full source code of the assignment file to align imports, class/function names, and behaviors. "
            "Constraints: minimal imports, deterministic behavior, no I/O, keep tests short and readable. "
            "Hard limit: produce at most 4 tests total across all lists; prefer filling 'test_methods' first, then leave other lists empty if the limit would be exceeded. "
            "Style: concise descriptions and names. Output must be valid JSON only. "
            "When a learning_path.md reference is provided, prioritize covering behaviors and examples mentioned there. "
            "Variant-specific rules: If assignment_ctx.variant == 'a' (case-insensitive), generate a TEST TEMPLATE for students: "
            "keep test names and docstrings, set GIVEN/WHEN/THEN sections to TODO placeholders. Tests should be incomplete and FAIL by default (do NOT skip). "
            "If assignment_ctx.variant == 'b', generate fully implemented tests that will initially fail until students implement assignment_b.py."
        )
        lp_md = module.get("learning_path_md", "")
        lp_note = "Use the learning path reference to choose assertions and edge cases." if lp_md else "No learning path reference provided. Use assignment_ctx and source code only."
        prompt = f"""
        Given the following assignment for module {module['title']}:

        - Variant: {assignment_ctx.get('variant')}
        - Declared class_name (if provided): {assignment_ctx.get('class_name')}

        Assignment source code (verbatim):
        ---
        {assignment_ctx.get('source_code', '')}
        ---

        Create JSON for keys used by test_template: test_target_name, test_target_description, test_imports[], module_path, class_name, test_coverage_areas[], fixtures[], test_methods[] (name, description, tests, given_section, when_section, then_section), parametrized_tests[], error_tests[], integration_tests[], performance_tests[], test_utilities[].

    Rules:
        - Infer the public API (class and method names) from the source code when present; prefer assignment_ctx.class_name if both are present but keep names consistent.
        - Set module_path to the package module path (e.g., module_{{module_number}}_{{module_name}}) not a file path; the package's __init__.py re-exports classes.
        - Keep imports minimal; prefer importing only pytest and the target class from module_path.
    - Respect the variant rules stated above; for variant 'a' produce TODO sections that lead to FAILING tests until implemented.

        {lp_note}

        Reference - learning_path.md:
        ---
        {lp_md}
        ---

        JSON only.
        """
        try:
            import json

            raw = self._complete(system, prompt)
            data = json.loads(raw)
            return data
        except Exception:
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator

            data = FallbackContentGenerator().tests_for_assignment(topic, module, assignment_ctx)
            return data

    # New AI-driven generators returning full file contents
    def readme(self, topic: dict) -> str:
        system = (
            "You are an expert course author. Generate a clear, friendly README.md for a programming lesson. "
            "Style: crisp and skimmable; short sections, short sentences, avoid verbosity. "
            "Prefer actionable steps and minimal commands. Include a Resources section at the end that lists documentation links, example repositories, and additional reading with Markdown links when available."
        )
        prompt = f"""
        Create a complete README.md for the lesson below. Use concise sections: overview, structure, learning objectives, getting started (venv + pip), testing commands, resources, and next steps.
        Use Markdown, no front matter. Keep it deterministic and runnable. Avoid making up commands beyond pytest/make targets shown.

        Topic JSON:
        {topic}
        """
        try:
            return self._complete(system, prompt, temperature=0.5)
        except Exception:
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator

            return FallbackContentGenerator().readme(topic)

    def extra_exercises(self, topic: dict, module: dict, module_number: int) -> str:
        system = (
            "You are a rigorous instructor. Generate extra practice exercises for a module. "
            "Style: concise prompts with clear goals and brief hints; avoid long narratives."
        )
        prompt = f"""
        Produce a Markdown file titled 'Extra Exercises - Module {module_number}: {module['title']}'. Provide 5-8 graded challenges from easy to hard, each with: brief goal, hints, and an optional stretch idea. No solutions.
        Context:
        Topic: {topic['title']}
        Module: {module['title']}
        Focus Areas: {', '.join(module.get('focus_areas', []))}
        """
        try:
            return self._complete(system, prompt, temperature=0.6)
        except Exception:
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator

            return FallbackContentGenerator().extra_exercises(topic, module, module_number)

    def starter_smoke_test(self, module_path: str, class_name: str | None, methods: list[dict] | None = None) -> str:
        system = (
            "You are an experienced Python tester. Generate concise pytest tests for a starter example class. "
            "Goal: cover the trivial demo() and at least one topic-relevant method if available. "
            "Constraints: small tests (2-4), deterministic, no I/O, no external deps. Keep code clear and minimal."
        )
        # Summarize methods (names only) for AI context; avoid leaking complex structures
        method_names = ", ".join([str((m or {}).get('name')) for m in (methods or []) if (m or {}).get('name') and not str((m or {}).get('name')).startswith('_')]) or ""
        if class_name:
            prompt = f"""
            Write a short pytest file that:
            - imports {class_name} from {module_path}
            - asserts that calling demo() returns 'ok'
            - if method names are provided, adds 1-2 additional small tests that exercise those methods at a basic level
            Provided public methods (names only): {method_names}
            Avoid helpers and fixtures unless essential. Only output test code.
            """
        else:
            prompt = f"""
            Write a short pytest file that:
            - imports the module as 'mod' from {module_path}
            - asserts that calling mod.demo() returns 'ok'
            Keep it concise and deterministic. Only output test code.
            """
        try:
            code = self._complete(system, prompt, temperature=0.2)
            return code
        except Exception:
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator
            return FallbackContentGenerator().starter_smoke_test(module_path, class_name, methods)

    def plan_modules(self, topic_name: str, desired_count: int | None = None) -> Dict[str, Any]:
        """Use the model to propose a module outline for a given topic.

        Returns a dict with keys: modules[], learning_objectives[], key_concepts[], resources{}
        """
        count = int(desired_count or 5)
        system = (
            "You are an expert curriculum designer for Python programming courses. "
            "Goal: cover as much of the topic as possible with the given number of modules. "
            "Distribute distinct, non-overlapping focus_areas across modules to maximize breadth; "
            "avoid repeating the same focus unless necessary. When modules < needed, prioritize the most impactful subtopics; "
            "when modules > subtopics, split major areas into progressively deeper facets. "
            "Produce a compact, pragmatic plan. Style: concise field values and short titles; avoid verbosity. "
            "Output must be valid JSON only."
        )
        prompt = f"""
        Propose a short module plan for a lesson about: {topic_name}
        Provide JSON with keys:
        - learning_objectives: array of 3-6 concise objectives
        - key_concepts: array of 1-5 key concepts
        - resources: object with documentation_links[], example_repositories[], additional_reading[]
        - modules: array of exactly {count} items; each item: {{
            name: snake_case short name,
            title: readable title,
            type: one of [starter, assignment, project],
            focus_areas: array of 1-3 short focus keys,
            complexity: simple|moderate|complex,
            estimated_time: integer minutes between 30 and 180,
            includes_tests: boolean,
            code_examples: small integer 1..5
        }}
        JSON only, no commentary.
        """
        try:
            import json

            raw = self._complete(system, prompt, temperature=0.6)
            data = json.loads(raw)
            # Minimal validation/normalization
            data["modules"] = data.get("modules") or []
            return data
        except Exception:
            if not self.allow_fallbacks:
                raise
            from lesson_generator.content import FallbackContentGenerator

            return FallbackContentGenerator().plan_modules(topic_name, desired_count)
