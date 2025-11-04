from __future__ import annotations

from lesson_generator.core.topic_processor import TopicProcessor, TopicModel, ModuleModel


def test_topic_and_module_names_are_normalized():
    # Free-form names with spaces, punctuation, and leading digit
    raw_topic_name = "  123 My Great Topic!  "
    raw_module_name = "  (Intro) Basics++  "

    topic = TopicModel(
        name=raw_topic_name,
        title="My Great Topic",
        description="desc",
        difficulty="beginner",
        estimated_hours=2,
        learning_objectives=["lo"],
        key_concepts=["kc"],
        modules=[
            ModuleModel(
                name=raw_module_name,
                title="Basics",
                type="starter",
                focus_areas=["fa"],
                complexity="simple",
                estimated_time=60,
            )
        ],
    )

    # Name fields should be normalized to lowercase snake-ish identifiers
    assert topic.name.startswith("t_") or topic.name[0].isalpha()
    assert topic.name == topic.name.lower()
    assert all(c.isalnum() or c == "_" for c in topic.name)

    assert topic.modules[0].name.startswith("m_") or topic.modules[0].name[0].isalpha()
    assert topic.modules[0].name == topic.modules[0].name.lower()
    assert all(c.isalnum() or c == "_" for c in topic.modules[0].name)


def test_from_names_preserves_human_title():
    tp = TopicProcessor()
    topics = tp.from_names(["Amazing THING 42!!!"])  # free-form input
    t = topics[0]
    # Title should be human-friendly
    assert t.title == "Amazing Thing 42!!!".title()  # Title-cased
    # Name should be normalized
    assert t.name == t.name.lower()
    assert all(c.isalnum() or c == "_" for c in t.name)
