from __future__ import annotations

from pathlib import Path

from lesson_generator.core.generator import LessonGenerator, GenerationOptions
from lesson_generator.core.topic_processor import ModuleModel, TopicModel
from lesson_generator.content import FallbackContentGenerator


def test_generator_creates_module_files(tmp_path: Path):
    topic = TopicModel(
        name="async_programming",
        title="Async Programming",
        description="Learn async",
        difficulty="beginner",
        estimated_hours=4,
        learning_objectives=["understand", "apply", "test"],
        key_concepts=["asyncio"],
        modules=[
            ModuleModel(
                name="basics",
                title="Basics",
                type="starter",
                focus_areas=["async_await"],
                complexity="simple",
                estimated_time=60,
            ),
            ModuleModel(
                name="advanced",
                title="Advanced",
                type="assignment",
                focus_areas=["tasks"],
                complexity="moderate",
                estimated_time=90,
            ),
        ],
    )

    import json

    gen = LessonGenerator(content_generator=FallbackContentGenerator())
    res = gen.generate(
        topics=None,
        topics_json=json.dumps(topic.model_dump()),
        options=GenerationOptions(output_dir=tmp_path, dry_run=False),
    )

    assert res.items[0].success
    root = tmp_path / topic.name
    # Module 1 files
    m1 = root / "module_1_basics"
    assert (m1 / "README.md").exists()
    assert (m1 / "starter_example.py").exists()
    assert (m1 / "assignment_a.py").exists()
    assert (m1 / "test_assignment_a.py").exists()

    # Module 2 (type assignment) should also have assignment_b and its tests
    m2 = root / "module_2_advanced"
    assert (m2 / "assignment_b.py").exists()
    assert (m2 / "test_assignment_b.py").exists()
