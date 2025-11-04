import json
import time

import pytest

from lesson_generator.content.openai_generator import OpenAIContentGenerator
from lesson_generator.content import FallbackContentGenerator


def _topic_module_simple():
    topic = {
        "name": "async_programming",
        "title": "Async Programming",
        "description": "Learn async",
        "difficulty": "beginner",
        "estimated_hours": 4,
        "learning_objectives": ["understand", "apply", "test"],
        "key_concepts": ["asyncio"],
        "modules": [],
    }
    module = {
        "name": "basics",
        "title": "Basics",
        "type": "starter",
        "focus_areas": ["async_await"],
        "complexity": "simple",
        "estimated_time": 60,
    }
    return topic, module


def test_openai_generator_learning_path_success(monkeypatch):
    gen = OpenAIContentGenerator(api_key=None)

    def fake_complete(system, prompt, temperature=0.7):
        return json.dumps(
            {
                "introduction": "Intro",
                "concepts": {
                    "async_await": {
                        "philosophy": "desc",
                        "example_code": "print('x')",
                        "use_cases": ["a"],
                        "advantages": ["b"],
                    }
                },
                "practical_examples": [
                    {"title": "ex", "description": "d", "code": "pass", "key_points": ["k"]}
                ],
                "testing_areas": ["t"],
                "advanced_concepts": [],
            }
        )

    monkeypatch.setattr(OpenAIContentGenerator, "_complete", staticmethod(lambda s, p, temperature=0.7: fake_complete(s, p, temperature)))

    topic, module = _topic_module_simple()
    out = gen.learning_path(topic, module)
    assert "introduction" in out and "concepts" in out
    assert "async_await" in out["concepts"]


def test_openai_generator_starter_example_fallback_on_error(monkeypatch):
    gen = OpenAIContentGenerator(api_key=None)
    monkeypatch.setattr(OpenAIContentGenerator, "_complete", staticmethod(lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("fail"))))

    topic, module = _topic_module_simple()
    out = gen.starter_example(topic, module)
    fb = FallbackContentGenerator().starter_example(topic, module)
    assert out["class_name"] == fb["class_name"]


def test_openai_generator_tests_no_notice_required(monkeypatch):
    gen = OpenAIContentGenerator(api_key=None)
    monkeypatch.setattr(OpenAIContentGenerator, "_complete", staticmethod(lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("fail"))))

    topic, module = _topic_module_simple()
    assignment_ctx = FallbackContentGenerator().assignment(topic, module)
    out = gen.tests_for_assignment(topic, module, assignment_ctx)
    # Ensure core test structure is present (no AI notice required)
    assert "test_methods" in out and isinstance(out["test_methods"], list)


@pytest.mark.performance
def test_content_generation_performance_fallback():
    topic, module = _topic_module_simple()
    fb = FallbackContentGenerator()

    start = time.time()
    out = fb.learning_path(topic, module)
    duration = time.time() - start

    assert "concepts" in out and duration < 0.5
