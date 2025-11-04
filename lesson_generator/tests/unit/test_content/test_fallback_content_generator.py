from __future__ import annotations

from lesson_generator.content import FallbackContentGenerator


def test_fallback_generates_learning_path_minimal():
    gen = FallbackContentGenerator()
    topic = {"name": "x", "title": "X", "learning_objectives": ["a", "b", "c"]}
    module = {"name": "m", "title": "M", "focus_areas": ["fa"]}
    data = gen.learning_path(topic, module)
    assert "introduction" in data and data["concepts"]


def test_fallback_generates_assignment_and_tests():
    gen = FallbackContentGenerator()
    topic = {"name": "x", "title": "X"}
    module = {"name": "m", "title": "M", "focus_areas": ["fa"]}
    asg = gen.assignment(topic, module, variant="a")
    assert asg["class_name"].endswith("A")
    tests = gen.tests_for_assignment(topic, module, asg)
    assert tests["class_name"] == asg["class_name"]
