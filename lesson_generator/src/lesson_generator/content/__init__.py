"""Content generation interfaces and implementations.

This module defines the interfaces and base implementations for generating lesson content.
The main interfaces are:
- ContentGenerator: Protocol defining content generation methods
- FallbackContentGenerator: Default implementation for offline/test mode
"""
from __future__ import annotations

from typing import Protocol, Dict, Any, List, Optional

# Type aliases for clarity
ModuleDict = Dict[str, Any]
TopicDict = Dict[str, Any]
ContentDict = Dict[str, Any]


class ContentGenerator(Protocol):
    """Protocol defining methods required for lesson content generation."""
    
    def plan_modules(self, topic_name: str, desired_count: Optional[int] = None) -> ContentDict:
        """Return a structured plan for modules given a topic name.
        
        Args:
            topic_name: The name of the topic to plan modules for
            desired_count: Optional target number of modules to generate

        Returns:
            Dict containing:
            - modules: List[ModuleDict] with minimum fields:
                - name: Module identifier
                - title: Human readable title
                - type: Module type (starter, assignment, etc)
                - focus_areas: List of key areas covered
                - complexity: Optional difficulty indicator
                - estimated_time: Optional minutes estimate
                - includes_tests: Optional boolean
                - code_examples: Optional example count
            - learning_objectives: List[str] with key learning goals
            - key_concepts: List[str] of core concepts covered
            - resources: Optional dict with reference materials
        """
    def learning_path(self, topic: dict, module: dict) -> Dict[str, Any]:
        ...

    def starter_example(self, topic: dict, module: dict) -> Dict[str, Any]:
        ...

    def assignment(self, topic: dict, module: dict, variant: str = "a") -> Dict[str, Any]:
        ...

    def tests_for_assignment(self, topic: dict, module: dict, assignment_ctx: Dict[str, Any]) -> Dict[str, Any]:
        ...

    # New: Additional content to be AI-generated
    def readme(self, topic: dict) -> str:
        """Return full README.md markdown content for the topic."""
        ...

    def extra_exercises(self, topic: dict, module: dict, module_number: int) -> str:
        """Return full extra_exercises.md markdown for the module."""
        ...

    def starter_smoke_test(self, module_path: str, class_name: str | None, methods: list[dict] | None = None) -> str:
        """Return pytest code for test_starter_example.py targeting the starter class.

        May include multiple short tests that cover the implemented starter methods.
        The 'methods' list (if provided) contains method descriptors from the starter context.
        """
        ...


class FallbackContentGenerator:
    """Deterministic content used when AI is unavailable (for tests and offline mode)."""

    def plan_modules(self, topic_name: str, desired_count: int | None = None) -> Dict[str, Any]:
        count = int(desired_count or 5)
        name_lc = (topic_name or "").lower()
        # Topic-aware plan: tailor modules for common topics
        if any(k in name_lc for k in ["dry", "don't repeat yourself", "dont repeat yourself"]):
            modules: list[Dict[str, Any]] = []
            # Ensure we always have at least two DRY-focused modules
            planned = [
                {
                    "name": "introduction_to_dry",
                    "title": "Introduction to DRY",
                    "type": "starter",
                    "focus_areas": [
                        "duplication_smells",
                        "single_source_of_truth",
                        "helper_functions",
                    ],
                    "complexity": "simple",
                    "estimated_time": 60,
                    "includes_tests": True,
                    "code_examples": 3,
                },
                {
                    "name": "applying_dry_in_python",
                    "title": "Applying DRY in Python",
                    "type": "assignment",
                    "focus_areas": [
                        "refactoring_patterns",
                        "test_parametrization",
                        "fixture_reuse",
                    ],
                    "complexity": "moderate",
                    "estimated_time": 90,
                    "includes_tests": True,
                    "code_examples": 3,
                },
            ]
            # Fill up to desired count with generic DRY-themed modules
            extras = [
                ("practices", "DRY Practices"),
                ("anti_patterns", "Anti-Patterns and Tradeoffs"),
                ("tooling", "Tooling for Duplication Detection"),
            ]
            for i in range(max(0, count - len(planned))):
                nm, title = extras[i % len(extras)]
                planned.append(
                    {
                        "name": nm,
                        "title": title,
                        "type": "assignment",
                        "focus_areas": [nm],
                        "complexity": "moderate",
                        "estimated_time": 90,
                        "includes_tests": True,
                        "code_examples": 2,
                    }
                )
            modules.extend(planned[:count])
            plan: Dict[str, Any] = {
                "modules": modules,
                "learning_objectives": [
                    "Identify code duplication and its costs",
                    "Apply DRY via helpers, abstraction, and configuration",
                    "Use tests and fixtures to remove duplication",
                ],
                "key_concepts": [
                    "duplication",
                    "abstraction",
                    "single source of truth",
                    "refactoring",
                ],
                "resources": {
                    "documentation_links": [
                        {"title": "pytest Parametrization", "url": "https://docs.pytest.org/en/stable/parametrize.html"},
                        {"title": "Python Functions", "url": "https://docs.python.org/3/tutorial/controlflow.html#defining-functions"},
                    ],
                    "example_repositories": ["https://github.com/python/cpython"],
                    "additional_reading": [
                        "https://martinfowler.com/bliki/DontrackRepeatYourself.html",
                        "https://peps.python.org/pep-0008/",
                    ],
                },
            }
            return plan

        # Generic fallback for other topics
        modules: list[Dict[str, Any]] = []
        base_names = [
            "basics",
            "foundations",
            "patterns",
            "practices",
            "advanced",
            "applications",
            "testing",
            "performance",
            "security",
            "deployment",
        ]
        for i in range(count):
            name = base_names[i % len(base_names)] if i < len(base_names) else f"module_{i+1}"
            suffix = "" if i < len(base_names) else f"_{i+1}"
            mod_name = f"{name}{suffix}"
            mod: Dict[str, Any] = {
                "name": mod_name,
                "title": mod_name.replace("_", " ").title(),
                "type": "assignment" if i >= 1 else "starter",
                "focus_areas": [name],
                "complexity": "simple" if i == 0 else ("moderate" if i < 3 else "complex"),
                "estimated_time": 60 if i == 0 else 90,
                "includes_tests": True,
                "code_examples": 3,
            }
            modules.append(mod)

        return {
            "modules": modules,
            "learning_objectives": [
                f"Understand core concepts of {topic_name}",
                f"Apply {topic_name} to real-world problems",
                "Write and run tests for generated code",
            ],
            "key_concepts": [topic_name],
            "resources": {
                "documentation_links": [
                    "https://docs.python.org/3/",
                    "https://realpython.com/",
                ],
                "example_repositories": ["https://github.com/python/cpython"],
                "additional_reading": ["https://peps.python.org/pep-0008/"],
            },
        }

    def learning_path(self, topic: dict, module: dict) -> Dict[str, Any]:
        tname = (topic.get("name") or "").lower()
        mname = (module.get("name") or "").lower()
        focus_areas = list(module.get("focus_areas") or ["concept"])
        if any(k in tname for k in ["dry", "don't repeat yourself", "dont repeat yourself"]):
            if "introduction_to_dry" in mname:
                concepts = {
                    "duplication_smells": {
                        "philosophy": "Spot and label repetition (copy-paste, parallel branches, magic numbers).",
                        "example_code": """\
def total_price_a(items):\n    total = 0\n    for it in items:\n        total += it['price'] * 1.2  # tax\n    return total\n\n# same logic duplicated elsewhere\ndef total_price_b(items):\n    total = 0\n    for it in items:\n        total += it['price'] * 1.2\n    return total\n""",
                        "use_cases": ["CRUD endpoints", "tests with repeated setup"],
                        "advantages": ["Easier refactoring when identified early"],
                    },
                    "single_source_of_truth": {
                        "philosophy": "Centralize constants/config/logic to one authoritative place.",
                        "example_code": """\
TAX_RATE = 1.2\n\ndef price_with_tax(price):\n    return price * TAX_RATE\n""",
                        "use_cases": ["configuration", "formatting helpers"],
                        "advantages": ["Consistency", "Reduced bugs"],
                    },
                    "helper_functions": {
                        "philosophy": "Extract shared logic into small, well-named functions.",
                        "example_code": """\
def _compute_total(items, rate):\n    return sum(it['price'] * rate for it in items)\n\n# reuse in multiple places instead of duplicating loops\n""",
                        "use_cases": ["data processing", "validation"],
                        "advantages": ["Reusability", "Testability"],
                    },
                }
                return {
                    "introduction": f"This module introduces DRY principles for {topic.get('title', topic.get('name'))}.",
                    "concepts": concepts,
                    "practical_examples": [
                        {
                            "title": "Extract a helper",
                            "description": "Refactor duplicated price calculations into one function.",
                            "code": """\
TAX_RATE = 1.2\n\ndef price_with_tax(price):\n    return price * TAX_RATE\n\ndef total_price(items):\n    return sum(price_with_tax(it['price']) for it in items)\n""",
                            "key_points": ["single source of truth", "naming", "tests become simpler"],
                        }
                    ],
                    "testing_areas": ["happy path", "edge cases", "regression after refactor"],
                    "advanced_concepts": [],
                }
            else:
                # Applying DRY in Python
                concepts = {
                    "refactoring_patterns": {
                        "philosophy": "Use extract function/class, deduplicate branches, and template methods.",
                        "example_code": """\
def validate_user(d):\n    required = ['id', 'email']\n    missing = [k for k in required if k not in d]\n    return not missing\n""",
                        "use_cases": ["service layers", "cli scripts"],
                        "advantages": ["Maintainability", "Fewer bugs"],
                    },
                    "test_parametrization": {
                        "philosophy": "Replace repeated nearly-identical tests with @pytest.mark.parametrize.",
                        "example_code": """\
import pytest\n\n@pytest.mark.parametrize('raw,expected', [("1",1),("2",2),("10",10)])\ndef test_parse_int(raw, expected):\n    assert int(raw) == expected\n""",
                        "use_cases": ["input variations", "boundary conditions"],
                        "advantages": ["Concise tests", "Better coverage"],
                    },
                    "fixture_reuse": {
                        "philosophy": "Share setup across tests with fixtures instead of copy/paste.",
                        "example_code": """\
import pytest\n\n@pytest.fixture\ndef sample_items():\n    return [{'price': 2},{'price': 3}]\n""",
                        "use_cases": ["db setup", "config"],
                        "advantages": ["Less duplication", "Clarity"],
                    },
                }
                return {
                    "introduction": f"Apply DRY with concrete patterns and testing techniques.",
                    "concepts": concepts,
                    "practical_examples": [
                        {
                            "title": "Parametrize tests",
                            "description": "Collapse repeated tests into a table-driven form.",
                            "code": concepts["test_parametrization"]["example_code"],
                            "key_points": ["remove repetition", "communicate intent"],
                        }
                    ],
                    "testing_areas": ["parametrized cases", "fixture coverage", "error handling"],
                    "advanced_concepts": [],
                }

        # Generic fallback
        return {
            "introduction": f"This module introduces {module['title']} in the context of {topic.get('title', topic.get('name'))}.",
            "concepts": {
                key: {
                    "philosophy": f"Core idea of {key} for {topic.get('name')}",
                    "example_code": f"print('Example for {key}')",
                    "use_cases": ["basic usage", "edge case handling"],
                    "advantages": ["clarity", "simplicity"],
                }
                for key in focus_areas
            },
            "practical_examples": [
                {
                    "title": "Getting Started",
                    "description": "First steps to apply the concept",
                    "code": "def hello():\n    return 'world'",
                    "key_points": ["setup", "run"],
                }
            ],
            "testing_areas": ["happy path", "error handling", "edge cases"],
            "advanced_concepts": [],
        }

    def starter_example(self, topic: dict, module: dict) -> Dict[str, Any]:
        tname = (topic.get("name") or "").lower()
        class_name = f"{module['name'].title().replace('_','')}Helper"
        focus_areas = module.get("focus_areas") or []
        fa_desc = ", ".join(focus_areas) or "core concepts"
        if any(k in tname for k in ["dry", "don't repeat yourself", "dont repeat yourself"]):
            # DRY-focused starter: keep a trivial demo(), plus illustrate deduplication via a shared helper
            methods = [
                {
                    "name": "demo",
                    "parameters": "",
                    "docstring": "Basic sanity check that exercises the helper.",
                    "demonstrates": fa_desc,
                    "args": [],
                    "return_type": "str",
                    "return_description": "confirmation string",
                    "example_usage": "helper.demo()",
                    "example_output": "'ok'",
                    "explanation": "Keep this method trivial so the smoke test is stable.",
                    "implementation": "return 'ok'",
                },
                {
                    "name": "_format_greeting",
                    "parameters": ", first: str, last: str",
                    "docstring": "Internal helper used by multiple public methods (illustrates DRY).",
                    "args": [
                        {"name": "first", "type": "str", "description": "first name"},
                        {"name": "last", "type": "str", "description": "last name"},
                    ],
                    "return_type": "str",
                    "return_description": "formatted full name",
                    "example_usage": "helper._format_greeting('Ada','Lovelace')",
                    "example_output": "'Hello, Ada Lovelace!'",
                    "explanation": "Single source of truth for greeting format.",
                    "implementation": "return f'Hello, {first} {last}!'",
                },
                {
                    "name": "greet_user",
                    "parameters": ", first: str, last: str",
                    "docstring": "Public method that reuses _format_greeting (no duplicated formatting).",
                    "args": [
                        {"name": "first", "type": "str", "description": "first name"},
                        {"name": "last", "type": "str", "description": "last name"},
                    ],
                    "return_type": "str",
                    "return_description": "greeting",
                    "example_usage": "helper.greet_user('Ada','Lovelace')",
                    "example_output": "'Hello, Ada Lovelace!'",
                    "explanation": "Demonstrates extraction of shared logic.",
                    "implementation": "return self._format_greeting(first, last)",
                },
                {
                    "name": "greet_users",
                    "parameters": ", names: list[tuple[str,str]]",
                    "docstring": "Batch greeting using the same helper to avoid repeating format code.",
                    "args": [
                        {"name": "names", "type": "list[tuple[str,str]]", "description": "(first,last) pairs"},
                    ],
                    "return_type": "list[str]",
                    "return_description": "list of greetings",
                    "example_usage": "helper.greet_users([('Ada','Lovelace'),('Grace','Hopper')])",
                    "example_output": "[ 'Hello, Ada Lovelace!', 'Hello, Grace Hopper!' ]",
                    "explanation": "Show DRY at small scale by reusing the same helper.",
                    "implementation": "return [self._format_greeting(f, l) for f, l in (names or [])]",
                },
            ]
            return {
                "title": f"{module['title']} Starter",
                "description": f"DRY-focused example for {module['title']} in {topic.get('title', topic.get('name'))}.",
                "learning_objectives": topic.get("learning_objectives", [])[:3],
                "detailed_explanation": "Illustrates removing duplication by extracting a single helper used in multiple methods.",
                "imports": ["from typing import Any, Iterable, Optional"],
                "class_name": class_name,
                "class_description": f"Demonstrates {fa_desc} with simple, testable methods.",
                "concepts": focus_areas,
                "methods": methods,
                "demonstrations": [
                    {"function_call": "print('Demo:', " + class_name + "().demo())"},
                    {"function_call": "print('Greet Ada =', " + class_name + "().greet_user('Ada','Lovelace'))"},
                ],
            }

        # Generic starter fallback with difficulty-calibrated method count
        diff = (topic.get("difficulty") or "intermediate").lower()
        methods: list[Dict[str, Any]] = [
            {
                "name": "demo",
                "parameters": "",
                "docstring": "Basic sanity check that exercises the helper.",
                "demonstrates": fa_desc,
                "args": [],
                "return_type": "str",
                "return_description": "confirmation string",
                "example_usage": "helper.demo()",
                "example_output": "'ok'",
                "explanation": "Keep this method trivial so the smoke test is stable.",
                "implementation": "return 'ok'",
            },
        ]
        if diff in {"intermediate", "advanced"}:
            methods.append(
                {
                    "name": "square",
                    "parameters": ", x: int",
                    "docstring": "Return the square of x.",
                    "demonstrates": fa_desc,
                    "args": [{"name": "x", "type": "int", "description": "input number"}],
                    "return_type": "int",
                    "return_description": "x squared",
                    "example_usage": "helper.square(4)",
                    "example_output": "16",
                    "explanation": "Tiny deterministic computation.",
                    "implementation": "return int(x) * int(x)",
                }
            )
        if diff == "advanced":
            methods.append(
                {
                    "name": "sum_nonnegatives",
                    "parameters": ", data: list[int] | None = None",
                    "docstring": "Sum only non-negative integers from a list.",
                    "demonstrates": fa_desc,
                    "args": [
                        {
                            "name": "data",
                            "type": "list[int] | None",
                            "description": "sequence of integers (optional)",
                        }
                    ],
                    "return_type": "int",
                    "return_description": "sum of non-negative values",
                    "example_usage": "helper.sum_nonnegatives([-2,-1,0,1,2])",
                    "example_output": "3",
                    "explanation": "Slightly richer logic with a small edge case.",
                    "implementation": "return sum(v for v in (data or []) if (v is not None and int(v) >= 0))",
                }
            )

        return {
            "title": f"{module['title']} Starter",
            "description": f"Fully functional example for {module['title']} in {topic.get('title', topic.get('name'))}.",
            "learning_objectives": topic.get("learning_objectives", [])[:3],
            "detailed_explanation": "Practical, runnable API to demonstrate the module topic end-to-end.",
            "imports": ["from typing import Any, Iterable, Optional"],
            "class_name": class_name,
            "class_description": f"Demonstrates {fa_desc} with simple, testable methods.",
            "concepts": focus_areas,
            "methods": methods,
            "demonstrations": [
                {"function_call": "print('Demo:', " + class_name + "().demo())"},
            ],
        }

    def assignment(self, topic: dict, module: dict, variant: str = "a") -> Dict[str, Any]:
        class_name = f"{module['name'].title().replace('_','')}Assignment{variant.upper()}"
        focus_areas = module.get("focus_areas") or []
        diff = (topic.get("difficulty") or "intermediate").lower()
        # Variant-specific implementation for primary method
        impl_process = (
            "raise NotImplementedError('implement assignment B')"
            if (variant or "a").lower() == "b"
            else "return sum(data or [])"
        )

        methods: list[Dict[str, Any]] = [
            {
                "name": "process",
                "parameters": ", data: Iterable[int] | None = None",
                "docstring": "Process input data and return a result.",
                "args": [
                    {"name": "data", "type": "Iterable[int] | None", "description": "numbers to process"}
                ],
                "return_type": "int",
                "return_description": "computed value",
                "examples": [{"usage": f"{class_name}().process([1,2,3])", "expected_output": "6"}],
                "implementation": impl_process,
            }
        ]

        # Difficulty-driven extra small method(s), keeping deterministic behavior and stable API
        if diff in {"intermediate", "advanced"}:
            impl_count = (
                "raise NotImplementedError('implement count')"
                if (variant or "a").lower() == "b"
                else "return len(list(data or []))"
            )
            methods.append(
                {
                    "name": "count",
                    "parameters": ", data: Iterable[int] | None = None",
                    "docstring": "Count number of items.",
                    "args": [
                        {"name": "data", "type": "Iterable[int] | None", "description": "sequence"}
                    ],
                    "return_type": "int",
                    "return_description": "count",
                    "examples": [{"usage": f"{class_name}().count([1,2,3])", "expected_output": "3"}],
                    "implementation": impl_count,
                }
            )
        if diff == "advanced":
            impl_sum_pos = (
                "raise NotImplementedError('implement sum_positive')"
                if (variant or "a").lower() == "b"
                else "return sum(x for x in (data or []) if int(x) > 0)"
            )
            methods.append(
                {
                    "name": "sum_positive",
                    "parameters": ", data: Iterable[int] | None = None",
                    "docstring": "Sum only positive integers.",
                    "args": [
                        {"name": "data", "type": "Iterable[int] | None", "description": "sequence"}
                    ],
                    "return_type": "int",
                    "return_description": "sum of positives",
                    "examples": [{"usage": f"{class_name}().sum_positive([-1,0,2,3])", "expected_output": "5"}],
                    "implementation": impl_sum_pos,
                }
            )

        return {
            "title": f"Assignment {variant.upper()} - {module['title']}",
            "description": f"Implement core functions for {module['title']}.",
            "imports": ["from typing import Optional, Iterable"],
            "class_name": class_name,
            "class_description": f"Solution skeleton for {module['title']}",
            "learning_focus": f"Focus: {', '.join(focus_areas)}",
            "methods": methods,
            "helper_functions": [],
            "examples": [
                {"description": "basic run", "code": f"print({class_name}().process([1,2,3]))"}
            ],
        }

    def tests_for_assignment(self, topic: dict, module: dict, assignment_ctx: Dict[str, Any]) -> Dict[str, Any]:
        """Generate test cases for assignments with guaranteed minimum test coverage."""
        class_name = assignment_ctx["class_name"]
        # Build module import path using provided module_number when available (defaults to 1)
        try:
            module_number = int(module.get("module_number") or 1)
        except Exception:
            module_number = 1
        module_path = f"module_{module_number}_{module['name']}"
        
        # Check if this should be a template (variant A) or complete tests (variant B)
        is_variant_a = (assignment_ctx.get("variant") or "a").lower() == "a"
        is_template_mode = is_variant_a or assignment_ctx.get("is_template", False)
        
        # Extract methods from source code or assignment context for test generation
        methods = []
        try:
            if assignment_ctx.get("source_code"):
                import ast
                tree = ast.parse(assignment_ctx["source_code"])
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and not node.name.startswith('_'):
                        methods.append({"name": node.name})
        except Exception:
            # Fall back to extracting from methods list if AST parsing fails
            try:
                methods = [{"name": m["name"]} for m in assignment_ctx.get("methods", [])]
            except Exception:
                pass

        base_result = {
            "test_target_name": f"{class_name}",
            "test_target_description": assignment_ctx.get("description", "Assignment implementation"),
            "test_imports": [],
            "module_path": module_path,
            "class_name": class_name,
            "test_coverage_areas": ["happy path", "empty input", "error handling"],
            "fixtures": [],
            "parametrized_tests": [],
            "error_tests": [],
            "integration_tests": [],
            "performance_tests": [],
            "test_utilities": [],
        }
        
        if is_template_mode:
            # For Assignment A: Generate template tests with TODO placeholders for students to fill in
            base_result.update({
                "is_template": True,
                "test_instructions": (
                    "Write focused pytest tests for the assignment below.\n"
                    "Each test should follow GIVEN / WHEN / THEN structure.\n"
                    "Replace the TODO sections with actual test implementation.\n"
                    "Ensure your tests cover: happy path, edge cases, and error handling."
                ),
                "test_methods": [
                    {
                        "name": "happy_path",
                        "description": "Test the main functionality with valid inputs",
                        "tests": "basic functionality",
                        "given_section": f"obj = {class_name}()",
                        "when_section": "# TODO: call the method under test with valid inputs",
                        "then_section": "assert False, \"TODO: replace with expected assertion for happy path\"",
                    },
                    {
                        "name": "edge_case_input",
                        "description": "Test behavior with edge case or boundary inputs",
                        "tests": "edge case handling",
                        "given_section": f"obj = {class_name}()",
                        "when_section": "# TODO: call the method with edge-case input (empty, None, etc.)",
                        "then_section": "assert False, \"TODO: implement edge-case assertion\"",
                    },
                    {
                        "name": "error_handling",
                        "description": "Test error handling and validation",
                        "tests": "error conditions",
                        "given_section": f"obj = {class_name}()",
                        "when_section": "# TODO: call the method in a way that should trigger error handling",
                        "then_section": "assert False, \"TODO: assert expected exception or error behavior\"",
                    },
                ]
            })
        else:
            # For Assignment B: Generate complete, working tests that will fail until students implement assignment_b.py
            base_result.update({
                "is_template": False,
                "test_methods": [
                    {
                        "name": "process_works_with_valid_data",
                        "description": "Should process valid data correctly",
                        "tests": "basic functionality",
                        "given_section": f"obj = {class_name}()",
                        "when_section": "result = obj.process([1, 2, 3])",
                        "then_section": "assert result == 6  # Expected sum of inputs",
                    },
                    {
                        "name": "process_handles_empty_input",
                        "description": "Should handle empty or None input gracefully",
                        "tests": "edge case handling",
                        "given_section": f"obj = {class_name}()",
                        "when_section": "result = obj.process(None)",
                        "then_section": "assert result == 0  # Expected default for empty input",
                    },
                    {
                        "name": "process_validates_input_type",
                        "description": "Should validate input types appropriately",
                        "tests": "error handling",
                        "given_section": f"obj = {class_name}()",
                        "when_section": "# Test with invalid input type\nresult = obj.process(\"invalid\")",
                        "then_section": "assert result is not None  # Expect some reasonable handling",
                    },
                ]
            })
        
        return base_result

    # New fallback implementations returning deterministic content
    def readme(self, topic: dict) -> str:
        lines = [
            f"# {topic.get('title')}",
            "",
            topic.get("description", ""),
            "",
            "## 📚 Course Overview",
            f"This lesson includes {len(topic.get('modules', []))} module(s) covering {', '.join(topic.get('key_concepts', []))}.",
            "",
            "## 🎯 Learning Objectives",
        ]
        for obj in topic.get("learning_objectives", []):
            lines.append(f"- {obj}")
        lines.extend([
            "",
            "## 🚦 Getting Started",
            "1. Read Module 1 learning_path.md",
            "2. Run starter_example.py",
            "3. Complete assignments and run tests",
        ])
        return "\n".join(lines) + "\n"

    def extra_exercises(self, topic: dict, module: dict, module_number: int) -> str:
        title = module.get("title") or module.get("name", "Module")
        return (
            f"# Extra Exercises - Module {module_number}: {title}\n\n"
            "Try these additional challenges to deepen your understanding:\n\n"
            "1. Implement a variant with different inputs\n"
            "2. Add error handling for edge cases\n"
            "3. Write property-based tests for robustness\n"
        )

    def starter_smoke_test(self, module_path: str, class_name: str | None, methods: list[dict] | None = None) -> str:
        # Basic header
        lines = [
            f'"""',
            f"Tests for starter example {class_name or module_path}",
            "",
            "Covers the trivial demo() and basic interface presence of topic methods.",
            '"""',
            "",
            (f"from {module_path} import {class_name}" if class_name else f"import {module_path} as _mod"),
            "",
        ]
        # demo() test
        lines += [
            "def test_demo_returns_ok():",
            (f"    obj = {class_name}()\n    assert obj.demo() == 'ok'" if class_name else "    assert _mod.demo() == 'ok'"),
            "",
        ]
        # If methods provided, add a light interface test to assert methods exist
        pub_methods: list[str] = []
        try:
            for m in (methods or []):
                name = (m or {}).get("name") or ""
                if name and not str(name).startswith("_"):
                    pub_methods.append(str(name))
        except Exception:
            pub_methods = []
        if pub_methods:
            lines += [
                "def test_public_methods_exist():",
                (f"    obj = {class_name}()" if class_name else f"    # Methods exist only on class; skip when no class is provided"),
                *([f"    assert hasattr(obj, '{nm}')" for nm in pub_methods] if class_name else []),
                "",
            ]
        return "\n".join(lines)


class CachedContentGenerator:
    """Simple caching wrapper for ContentGenerator to avoid repeated work.

    Caches by (method, topic['name'], module['name'], variant?) where applicable.
    If underlying generator is None, uses FallbackContentGenerator.
    """

    def __init__(self, underlying: ContentGenerator | None) -> None:
        self._underlying: ContentGenerator = underlying or FallbackContentGenerator()  # type: ignore[assignment]
        # Cache can hold either dicts or plain strings depending on method
        self._cache: Dict[tuple, Any] = {}

    def _key(self, method: str, topic: dict, module: dict, variant: str | None = None) -> tuple:
        return (
            method,
            topic.get("name"),
            module.get("name"),
            variant,
        )

    # Planning doesn't fit topic/module pair cache key, provide dedicated cache
    def plan_modules(self, topic_name: str, desired_count: int | None = None) -> Any:
        k = ("plan_modules", topic_name, desired_count)
        if k not in self._cache:
            # Build a minimal topic-like dict for compatibility with underlying generators that may rely on it
            self._cache[k] = self._underlying.plan_modules(topic_name, desired_count)
        return self._cache[k]

    def learning_path(self, topic: dict, module: dict) -> Dict[str, Any]:
        k = self._key("learning_path", topic, module)
        if k not in self._cache:
            self._cache[k] = self._underlying.learning_path(topic, module)
        return self._cache[k]

    def starter_example(self, topic: dict, module: dict) -> Dict[str, Any]:
        k = self._key("starter_example", topic, module)
        if k not in self._cache:
            self._cache[k] = self._underlying.starter_example(topic, module)
        return self._cache[k]

    def assignment(self, topic: dict, module: dict, variant: str = "a") -> Dict[str, Any]:
        k = self._key("assignment", topic, module, variant)
        if k not in self._cache:
            self._cache[k] = self._underlying.assignment(topic, module, variant)
        return self._cache[k]

    def tests_for_assignment(self, topic: dict, module: dict, assignment_ctx: Dict[str, Any]) -> Dict[str, Any]:
        # tests depend on assignment_ctx, so include class_name in the key
        k = self._key("tests_for_assignment", topic, module, assignment_ctx.get("class_name"))
        if k not in self._cache:
            self._cache[k] = self._underlying.tests_for_assignment(topic, module, assignment_ctx)
        return self._cache[k]

    # New cached methods
    def readme(self, topic: dict) -> str:
        k = ("readme", topic.get("name"))
        if k not in self._cache:
            self._cache[k] = self._underlying.readme(topic)
        return self._cache[k]

    def extra_exercises(self, topic: dict, module: dict, module_number: int) -> str:
        k = ("extra_exercises", topic.get("name"), module.get("name"), module_number)
        if k not in self._cache:
            self._cache[k] = self._underlying.extra_exercises(topic, module, module_number)
        return self._cache[k]

    def starter_smoke_test(self, module_path: str, class_name: str | None, methods: list[dict] | None = None) -> str:
        # Use method names as part of the cache key to account for interface changes
        method_names = tuple((m.get("name") if isinstance(m, dict) else None) for m in (methods or []))
        k = ("starter_smoke_test", module_path, class_name or "_", method_names)
        if k not in self._cache:
            self._cache[k] = self._underlying.starter_smoke_test(module_path, class_name, methods)
        return self._cache[k]
