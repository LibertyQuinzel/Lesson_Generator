from __future__ import annotations

import json
import pytest

from lesson_generator.core.topic_processor import TopicProcessor, TopicValidationError, TopicModel, ModuleModel


def test_parse_topics_invalid_json_raises():
    tp = TopicProcessor()
    with pytest.raises(TopicValidationError):
        tp.parse_topics("{ this is not json }")


def test_invalid_difficulty_raises():
    bad = {
        "name": "ok_name",
        "title": "Ok Name",
        "description": "desc",
        "difficulty": "expert",  # invalid
        "estimated_hours": 2,
        "learning_objectives": ["lo"],
        "key_concepts": ["kc"],
        "modules": [
            {
                "name": "m",
                "title": "M",
                "type": "starter",
                "focus_areas": ["fa"],
                "estimated_time": 60,
            }
        ],
    }
    tp = TopicProcessor()
    with pytest.raises(TopicValidationError):
        tp.parse_topics(json.dumps(bad))
