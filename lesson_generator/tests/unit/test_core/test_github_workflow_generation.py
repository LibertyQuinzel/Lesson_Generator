from __future__ import annotations

from pathlib import Path

from lesson_generator.core.generator import LessonGenerator, GenerationOptions
from lesson_generator.core.topic_processor import ModuleModel, TopicModel
from lesson_generator.content import FallbackContentGenerator


def test_generator_adds_github_workflow_and_gitignore(tmp_path: Path):
    topic = TopicModel(
        name="ci_ready_topic",
        title="CI Ready Topic",
        description="desc",
        difficulty="beginner",
        estimated_hours=1,
        learning_objectives=["lo"],
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
    # .gitignore present
    assert (root / ".gitignore").exists()
    # GitHub Actions workflow present
    assert (root / ".github" / "workflows" / "python-tests.yml").exists()
