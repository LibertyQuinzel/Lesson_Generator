"""Topic models and processing utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel, Field, ValidationError, field_validator


def _to_snake_lower(text: str, *, prefix_if_invalid: str = "m") -> str:
    """Convert arbitrary text to a safe snake_case-ish identifier in lowercase.

    - Lowercases the text
    - Replaces any non-alphanumeric character with underscore
    - Collapses multiple underscores
    - Ensures it starts with a letter by prefixing if necessary
    - Strips leading/trailing underscores
    """
    import re as _re

    if not text:
        return prefix_if_invalid
    s = str(text).lower()
    s = _re.sub(r"[^a-z0-9]+", "_", s)
    s = _re.sub(r"_+", "_", s).strip("_")
    if not s:
        s = prefix_if_invalid
    if not s[0].isalpha():
        s = prefix_if_invalid + ("_" + s if s else "")
    return s


class ModuleModel(BaseModel):
    name: str
    title: str
    type: str
    focus_areas: List[str]
    complexity: Optional[str] = Field(default=None)
    estimated_time: Optional[int] = Field(default=None, ge=15, le=480)
    includes_tests: Optional[bool] = True
    code_examples: Optional[int] = Field(default=3, ge=1, le=10)

    # Normalize module.name to a safe snake_case-like lowercase identifier
    @field_validator("name")
    @classmethod
    def _normalize_module_name(cls, v: str) -> str:  # noqa: D401
        """Normalize module name to safe snake_case-like lowercase."""
        return _to_snake_lower(v, prefix_if_invalid="m")


class ResourcesModel(BaseModel):
    documentation_links: Optional[List[str]] = None
    example_repositories: Optional[List[str]] = None
    additional_reading: Optional[List[str]] = None


class TopicModel(BaseModel):
    name: str
    title: str
    description: str
    difficulty: str
    estimated_hours: int = Field(..., ge=1, le=40)
    prerequisites: Optional[List[str]] = None
    learning_objectives: List[str]
    key_concepts: List[str]
    programming_language: Optional[str] = "python"
    modules: List[ModuleModel]
    tags: Optional[List[str]] = None
    resources: Optional[ResourcesModel] = None

    @field_validator("difficulty")
    def _difficulty_allowed(cls, v: str) -> str:  # noqa: D401
        """Validate difficulty value."""
        allowed = {"beginner", "intermediate", "advanced"}
        if v not in allowed:
            raise ValueError(f"difficulty must be one of {sorted(allowed)}")
        return v

    @field_validator("name")
    def _normalize_topic_name(cls, v: str) -> str:  # noqa: D401
        """Normalize topic name to safe snake_case-like lowercase."""
        return _to_snake_lower(v, prefix_if_invalid="t")


class TopicValidationError(Exception):
    """Raised when topic configuration is invalid."""


class TopicProcessor:
    """Parses and validates topic definitions."""

    def parse_topics(self, payload: str | bytes) -> List[TopicModel]:
        import json

        try:
            data = json.loads(payload)
        except Exception as exc:  # pragma: no cover - exercised via CLI
            raise TopicValidationError(f"Invalid JSON: {exc}") from exc

        raw_list = data if isinstance(data, list) else [data]
        topics: List[TopicModel] = []
        for raw in raw_list:
            try:
                topics.append(TopicModel(**raw))
            except ValidationError as exc:
                raise TopicValidationError(str(exc)) from exc
        return topics

    def from_names(self, names: List[str]) -> List[TopicModel]:
        """Create minimal topic models from plain names (Sprint 1 convenience)."""
        topics: List[TopicModel] = []
        for name in names:
            # Preserve a human-friendly title from the raw input; name field will be normalized by validator
            title_readable = str(name).replace("_", " ").strip()
            if not title_readable:
                title_readable = "Lesson"
            title_readable = title_readable.title()
            topics.append(
                TopicModel(
                    name=str(name),
                    title=title_readable,
                    description=f"Auto-generated lesson for {title_readable}.",
                    difficulty="intermediate",
                    estimated_hours=4,
                    learning_objectives=[
                        f"Understand core concepts of {title_readable}",
                        f"Implement examples related to {title_readable}",
                        "Write and run tests",
                    ],
                    key_concepts=[str(name)],
                    modules=[
                        ModuleModel(
                            name="basics",
                            title="Basics",
                            type="starter",
                            focus_areas=["overview", "setup"],
                            complexity="simple",
                            estimated_time=60,
                        )
                    ],
                )
            )
        return topics

