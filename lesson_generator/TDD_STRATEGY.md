# Test-Driven Development (TDD) Strategy

## 🎯 Testing Philosophy

This project follows **strict TDD principles** with a focus on:
- **Red–Green–Blue (Refactor)** cycle for all new features ("Blue" == Refactor phase)
- **High test coverage** (minimum 95%)
- **Fast feedback loops** through comprehensive unit testing
- **Integration testing** for external service interactions
- **Contract testing** for API interfaces

## 🧪 Test Categories & Structure

### 1. **Unit Tests** (Fast, Isolated)
```
tests/unit/
├── test_cli/
│   ├── test_command_parser.py
│   ├── test_input_validator.py
│   └── test_progress_reporter.py
├── test_core/
│   ├── test_lesson_generator.py
│   ├── test_topic_processor.py
│   ├── test_template_engine.py
│   └── test_file_manager.py
├── test_content/
│   ├── test_openai_generator.py
│   ├── test_code_generator.py
│   ├── test_assignment_creator.py
│   └── test_test_generator.py
└── test_quality/
    ├── test_code_validator.py
    ├── test_linting_engine.py
    └── test_test_runner.py
```

### 2. **Integration Tests** (Component Interactions)
```
tests/integration/
├── test_openai_integration.py      # OpenAI API integration
├── test_file_system_integration.py # File I/O operations
├── test_template_rendering.py      # Template engine with real data
└── test_end_to_end_generation.py   # Complete lesson generation
```

### 3. **Contract Tests** (External APIs)
```
tests/contracts/
├── test_openai_contract.py         # OpenAI API contract validation
└── test_file_system_contract.py    # File system operation contracts
```

### 4. **Performance Tests** (Load & Stress)
```
tests/performance/
├── test_generation_speed.py        # Lesson generation performance
├── test_memory_usage.py           # Memory consumption tests
└── test_concurrent_generation.py   # Parallel processing tests
```

### 5. **Acceptance Tests** (E2E User Stories)
```
tests/acceptance/
├── test_basic_lesson_generation.py     # Happy path scenarios
├── test_error_handling.py              # Error scenarios
└── test_batch_processing.py            # Multiple lesson generation
```

## 🔄 TDD Workflow

### Phase 1: Red (Write Failing Tests)
```python
# Example: test_topic_processor.py
import pytest
from lesson_generator.core.topic_processor import TopicProcessor

class TestTopicProcessor:
    def test_should_parse_valid_topic_configuration(self):
        # GIVEN
        topic_config = {
            "name": "async_programming",
            "difficulty": "intermediate",
            "concepts": ["coroutines", "event_loops", "asyncio"]
        }
        processor = TopicProcessor()
        
        # WHEN
        result = processor.parse_topic(topic_config)
        
        # THEN
        assert result.name == "async_programming"
        assert result.difficulty == "intermediate"
        assert len(result.concepts) == 3
        # This test will FAIL initially (Red phase)
```

### Phase 2: Green (Make Tests Pass)
```python
# Implementation: topic_processor.py
from dataclasses import dataclass
from typing import List

@dataclass
class Topic:
    name: str
    difficulty: str
    concepts: List[str]

class TopicProcessor:
    def parse_topic(self, config: dict) -> Topic:
        return Topic(
            name=config["name"],
            difficulty=config["difficulty"],
            concepts=config["concepts"]
        )
        # Minimal implementation to make test pass (Green phase)
```

### Phase 3: Refactor (Improve Code Quality)
```python
# Refactored: topic_processor.py
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class Difficulty(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

@dataclass
class Topic:
    name: str
    difficulty: Difficulty
    concepts: List[str]
    estimated_hours: Optional[int] = None

class TopicValidationError(Exception):
    pass

class TopicProcessor:
    def parse_topic(self, config: dict) -> Topic:
        self._validate_config(config)
        return Topic(
            name=config["name"],
            difficulty=Difficulty(config["difficulty"]),
            concepts=config["concepts"],
            estimated_hours=config.get("estimated_hours")
        )
    
    def _validate_config(self, config: dict) -> None:
        required_fields = ["name", "difficulty", "concepts"]
        for field in required_fields:
            if field not in config:
                raise TopicValidationError(f"Missing required field: {field}")
        # Refactored with proper validation and type safety
```

## 🎭 Test Doubles Strategy

### 1. **Mocks** (External Dependencies)
```python
# test_openai_generator.py
import pytest
from unittest.mock import Mock, patch
from lesson_generator.content.openai_generator import OpenAIContentGenerator

class TestOpenAIContentGenerator:
    @patch('openai.OpenAI')
    def test_should_generate_learning_content_from_topic(self, mock_openai):
        # GIVEN
        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.return_value.choices[0].message.content = "Generated content"
        
        generator = OpenAIContentGenerator(api_key="test-key")
        topic = Topic(name="async_programming", difficulty="intermediate", concepts=["asyncio"])
        
        # WHEN
        result = generator.generate_learning_content(topic)
        
        # THEN
        assert "Generated content" in result.content
        mock_client.chat.completions.create.assert_called_once()
```

### 2. **Stubs** (Controlled Responses)
```python
# test_template_engine.py
class TestTemplateEngine:
    def test_should_render_learning_path_template(self, tmp_path):
        # GIVEN
        template_content = "# {{ topic.name }}\n{{ content.description }}"
        template_file = tmp_path / "learning_path.md.j2"
        template_file.write_text(template_content)
        
        engine = TemplateEngine(templates_dir=tmp_path)
        topic = Topic(name="Test Topic")
        content = LearningContent(description="Test description")
        
        # WHEN
        result = engine.render_learning_path(topic, content)
        
        # THEN
        assert "# Test Topic" in result
        assert "Test description" in result
```

### 3. **Fakes** (Working Test Implementations)
```python
# test_helpers/fake_openai_generator.py
class FakeOpenAIGenerator:
    def __init__(self):
        self.responses = {
            "async_programming": "Async programming content...",
            "design_patterns": "Design patterns content..."
        }
    
    def generate_learning_content(self, topic: Topic) -> LearningContent:
        content = self.responses.get(topic.name, "Default content")
        return LearningContent(description=content)
```

## 📊 Test Coverage Strategy

### Coverage Targets
- **Unit Tests**: 98% line coverage
- **Integration Tests**: 85% feature coverage
- **E2E Tests**: 100% user story coverage

### Coverage Configuration
```ini
# pytest.ini
[tool:pytest]
addopts = 
    --cov=src/lesson_generator
    --cov-report=html:htmlcov
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=95
    --strict-markers
    --strict-config

markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (slower, external deps)
    e2e: End-to-end tests (slowest, full system)
    performance: Performance and load tests
```

### Test Execution Strategy
```bash
# Fast feedback loop (unit tests only)
pytest tests/unit/ -m unit

# Integration testing
pytest tests/integration/ -m integration

# Full test suite
pytest

# Performance testing
pytest tests/performance/ -m performance --benchmark-only
```

## 🚀 Continuous Testing Pipeline

### Pre-commit Hooks
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: pytest-unit
        name: Run unit tests
        entry: pytest tests/unit/
        language: system
        pass_filenames: false
        
      - id: pytest-coverage
        name: Check test coverage
        entry: pytest --cov=src/lesson_generator --cov-fail-under=95
        language: system
        pass_filenames: false
```

### CI/CD Test Stages
```yaml
# .github/workflows/test.yml
name: Test Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
        pip install -e .
    
    - name: Run unit tests
      run: pytest tests/unit/ -v
    
    - name: Run integration tests
      run: pytest tests/integration/ -v
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    
    - name: Run coverage
      run: pytest --cov=src/lesson_generator --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
```

## 🧰 Test Utilities & Fixtures

### Shared Fixtures
```python
# conftest.py
import pytest
from pathlib import Path
from lesson_generator.core.topic_processor import Topic, TopicProcessor

@pytest.fixture
def sample_topic():
    return Topic(
        name="async_programming",
        difficulty="intermediate",
        concepts=["coroutines", "event_loops", "asyncio"]
    )

@pytest.fixture
def temp_lesson_dir(tmp_path):
    lesson_dir = tmp_path / "test_lesson"
    lesson_dir.mkdir()
    return lesson_dir

@pytest.fixture
def mock_openai_response():
    return {
        "choices": [{
            "message": {
                "content": "Generated learning content for testing"
            }
        }]
    }
```

### Test Data Builders
```python
# test_helpers/builders.py
class TopicBuilder:
    def __init__(self):
        self._name = "default_topic"
        self._difficulty = "beginner"
        self._concepts = ["basic_concept"]
    
    def with_name(self, name: str):
        self._name = name
        return self
    
    def with_difficulty(self, difficulty: str):
        self._difficulty = difficulty
        return self
    
    def with_concepts(self, concepts: List[str]):
        self._concepts = concepts
        return self
    
    def build(self) -> Topic:
        return Topic(
            name=self._name,
            difficulty=self._difficulty,
            concepts=self._concepts
        )

# Usage in tests
def test_complex_topic_processing():
    topic = (TopicBuilder()
             .with_name("advanced_async")
             .with_difficulty("advanced")
             .with_concepts(["asyncio", "aiohttp", "concurrent.futures"])
             .build())
```

## 🎯 Testing Best Practices

### Test Naming Convention
```python
def test_should_[expected_behavior]_when_[scenario]():
    pass

# Examples:
def test_should_generate_five_modules_when_topic_requires_comprehensive_coverage():
def test_should_raise_validation_error_when_topic_config_missing_required_fields():
def test_should_cache_openai_responses_when_same_topic_requested_multiple_times():
```

### Test Structure (Given-When-Then)
```python
def test_should_create_lesson_structure_when_valid_topic_provided():
    # GIVEN (Arrange)
    topic = sample_topic()
    generator = LessonGenerator()
    output_dir = temp_lesson_dir()
    
    # WHEN (Act)
    result = generator.generate_lesson(topic, output_dir)
    
    # THEN (Assert)
    assert result.success
    assert (output_dir / "module_1_async_basics").exists()
    assert (output_dir / "requirements.txt").exists()
```

### Parameterized Tests
```python
@pytest.mark.parametrize("topic_name,expected_modules", [
    ("async_programming", 5),
    ("design_patterns", 6),
    ("testing_strategies", 4),
])
def test_should_generate_correct_module_count_for_different_topics(topic_name, expected_modules):
    topic = Topic(name=topic_name, difficulty="intermediate", concepts=[])
    generator = LessonGenerator()
    
    result = generator.generate_lesson(topic, tmp_path)
    
    assert len(result.modules) == expected_modules
```