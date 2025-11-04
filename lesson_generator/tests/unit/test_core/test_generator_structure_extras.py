from __future__ import annotations

from pathlib import Path

from lesson_generator.core.generator import LessonGenerator, GenerationOptions
from lesson_generator.core.topic_processor import ModuleModel, TopicModel
from lesson_generator.content import FallbackContentGenerator


def test_generator_creates_extras_and_root_files(tmp_path: Path):
    topic = TopicModel(
        name="dp_topic",
        title="DP Topic",
        description="desc",
        difficulty="beginner",
        estimated_hours=2,
        learning_objectives=["lo1"],
        key_concepts=["kc"],
        modules=[
            ModuleModel(
                name="m1", title="M1", type="starter", focus_areas=["fa"], complexity="simple", estimated_time=30
            )
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
    # Root files from sprint 3
    assert (root / "Makefile").exists()
    assert (root / "setup.cfg").exists()

    mod = root / "module_1_m1"
    # Extras
    assert (mod / "test_starter_example.py").exists()
    assert (mod / "extra_exercises.md").exists()
