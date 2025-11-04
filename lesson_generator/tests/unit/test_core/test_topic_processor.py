from __future__ import annotations

from lesson_generator.core.topic_processor import TopicProcessor


def test_parse_minimal_topic_from_name():
    tp = TopicProcessor()
    topic = tp.from_names(["design_patterns"])[0]
    assert topic.name == "design_patterns"
    assert topic.difficulty == "intermediate"
    assert len(topic.modules) >= 1


def test_parse_topics_from_json_valid():
    payload = """
    {
        "name": "testing_strategies",
        "title": "Testing Strategies",
        "description": "Learn testing.",
        "difficulty": "beginner",
        "estimated_hours": 5,
        "learning_objectives": [
            "understand",
            "apply",
            "test"
        ],
        "key_concepts": ["pytest"],
        "modules": [
            {
                "name": "basics",
                "title": "Basics",
                "type": "starter",
                "focus_areas": ["intro"]
            }
        ]
    }
    """
    tp = TopicProcessor()
    topics = tp.parse_topics(payload)
    assert len(topics) == 1
    assert topics[0].name == "testing_strategies"
