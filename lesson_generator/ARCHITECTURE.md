# Lesson Generator - System Architecture

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    LESSON GENERATOR SYSTEM                  │
├─────────────────────────────────────────────────────────────┤
│  CLI Interface (Click)                                      │
│  ├── Command Parser                                         │
│  ├── Validation Layer                                       │
│  └── Progress Reporter                                       │
├─────────────────────────────────────────────────────────────┤
│  Core Generator Engine                                      │
│  ├── LessonGenerator (Main Orchestrator)                   │
│  ├── TopicProcessor (Topic → Content Mapping)              │
│  ├── TemplateEngine (Jinja2 Templates)                     │
│  └── FileStructureManager (Directory Creation)             │
├─────────────────────────────────────────────────────────────┤
│  Content Generation Layer                                   │
│  ├── OpenAI Content Generator                              │
│  ├── Code Example Generator                                │
│  ├── Assignment Creator                                     │
│  └── Test Case Generator                                    │
├─────────────────────────────────────────────────────────────┤
│  Quality Assurance Layer                                   │
│  ├── Code Validator (AST + Syntax Check)                   │
│  ├── Test Runner (Pytest Integration)                      │
│  ├── Linting Engine (Pylint + Black)                       │
│  └── Content Reviewer                                       │
├─────────────────────────────────────────────────────────────┤
│  Configuration & Templates                                  │
│  ├── Topic Configuration (JSON Schema)                     │
│  ├── Jinja2 Templates                                       │
│  ├── Code Templates                                         │
│  └── Test Templates                                         │
├─────────────────────────────────────────────────────────────┤
│  External Services                                          │
│  ├── OpenAI API (GPT-4 for content)                       │
│  ├── File System I/O                                       │
│  └── Git Integration (Optional)                            │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Component Architecture

### 1. **CLI Interface Layer**
- **Technology**: Click framework
- **Responsibilities**: 
  - Parse command-line arguments
  - Validate input parameters
  - Display progress and results
  - Handle error reporting
- **Key Components**:
  - `CommandParser`: Main CLI entry point
  - `InputValidator`: Validate topics, paths, configurations
  - `ProgressReporter`: Show generation progress

### 2. **Core Generator Engine**
- **Technology**: Pure Python with dependency injection
- **Responsibilities**:
  - Orchestrate the entire lesson generation process
  - Manage dependencies between components
  - Handle configuration and state management
- **Key Components**:
  - `LessonGenerator`: Main orchestrator class
  - `TopicProcessor`: Convert topics to structured data
  - `TemplateEngine`: Jinja2 template processing
  - `FileStructureManager`: Directory and file creation

### 3. **Content Generation Layer**
- **Technology**: OpenAI API + Python AST + Jinja2
- **Responsibilities**:
  - Generate topic-specific content using AI
  - Create code examples and assignments
  - Generate test cases and documentation
- **Key Components**:
  - `OpenAIContentGenerator`: AI-powered content creation
  - `CodeExampleGenerator`: Programming examples
  - `AssignmentCreator`: Student assignments
  - `TestCaseGenerator`: Unit test creation

### 4. **Quality Assurance Layer**
- **Technology**: AST, Pylint, Black, Pytest
- **Responsibilities**:
  - Validate generated code syntax
  - Ensure code quality standards
  - Run generated tests
  - Content consistency checks
- **Key Components**:
  - `CodeValidator`: Syntax and structure validation
  - `TestRunner`: Execute generated tests
  - `LintingEngine`: Code style enforcement
  - `ContentReviewer`: Content quality checks

## 🔄 Data Flow Architecture

```
Input (Topics + Config) 
    ↓
Topic Processing (Parse & Structure)
    ↓
Content Generation (OpenAI + Templates)
    ↓
Code Generation (Examples + Assignments)
    ↓
Quality Assurance (Validation + Testing)
    ↓
File System Output (Structured Lessons)
    ↓
Post-processing (Documentation + Packaging)
```

## 🗃️ Data Models

### Topic Configuration Schema
```json
{
  "topic": {
    "name": "string",
    "difficulty": "beginner|intermediate|advanced",
    "concepts": ["list", "of", "concepts"],
    "learning_objectives": ["list", "of", "objectives"],
    "prerequisites": ["list", "of", "prereqs"],
    "estimated_hours": "number",
    "modules": [
      {
        "name": "string",
        "type": "starter|assignment|extra",
        "focus_areas": ["list", "of", "areas"],
        "code_complexity": "simple|moderate|complex"
      }
    ]
  }
}
```

### Lesson Structure Schema
```json
{
  "lesson": {
    "title": "string",
    "description": "string",
    "modules": [
      {
        "name": "string",
        "files": {
          "learning_path": "content",
          "starter_example": "code",
          "assignment_a": "code",
          "assignment_b": "code",
          "test_files": ["list", "of", "test", "files"],
          "extra_exercises": "content"
        }
      }
    ],
    "config_files": ["requirements.txt", "pytest.ini", "Makefile"],
    "metadata": {
      "created_at": "timestamp",
      "generator_version": "string",
      "ai_model_used": "string"
    }
  }
}
```

## 🔌 Integration Points

### OpenAI API Integration
```python
class OpenAIContentGenerator:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.client = OpenAI(api_key=api_key)
        self.model = model
    
    async def generate_learning_content(self, topic: Topic) -> LearningContent:
        # Generate structured learning content
        pass
    
    async def generate_code_example(self, concept: str, difficulty: str) -> CodeExample:
        # Generate code examples
        pass
```

### Template Engine Integration
```python
class TemplateEngine:
    def __init__(self, templates_dir: Path):
        self.env = Environment(loader=FileSystemLoader(templates_dir))
    
    def render_learning_path(self, topic: Topic, content: LearningContent) -> str:
        # Render learning path markdown
        pass
    
    def render_assignment(self, assignment_data: AssignmentData) -> str:
        # Render assignment Python files
        pass
```

## 🚀 Scalability & Performance

### Concurrent Processing
- **Async/Await**: Use asyncio for OpenAI API calls
- **Thread Pools**: Parallel file I/O operations
- **Batch Processing**: Generate multiple lessons simultaneously

### Caching Strategy
- **Template Caching**: Cache compiled Jinja2 templates
- **API Response Caching**: Cache similar OpenAI responses
- **Configuration Caching**: Cache parsed topic configurations

### Resource Management
- **Rate Limiting**: Respect OpenAI API rate limits
- **Memory Management**: Stream large file operations
- **Error Resilience**: Retry mechanisms with exponential backoff

## 🛡️ Error Handling & Logging

### Error Categories
1. **Input Validation Errors**: Invalid topics, missing configurations
2. **API Errors**: OpenAI API failures, rate limiting
3. **File System Errors**: Permission issues, disk space
4. **Code Generation Errors**: Invalid syntax, template failures
5. **Quality Assurance Errors**: Test failures, lint issues

### Logging Strategy
```python
import structlog

logger = structlog.get_logger()

# Structured logging throughout the application
logger.info("lesson_generation_started", 
           topic=topic_name, 
           modules=module_count,
           timestamp=datetime.now())
```

## 🔒 Security Considerations

### API Key Management
- Environment variables for OpenAI API keys
- Key validation before processing
- Secure key storage recommendations

### Code Safety
- AST-based code validation before execution
- Sandboxed test execution
- Input sanitization for all user-provided data

### File System Security
- Path traversal prevention
- Permission checks before file operations
- Temporary directory cleanup

---

## 📁 Project Structure

```
lesson_generator/
├── src/
│   ├── lesson_generator/
│   │   ├── __init__.py
│   │   ├── cli/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   └── commands.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── generator.py
│   │   │   ├── topic_processor.py
│   │   │   └── file_manager.py
│   │   ├── content/
│   │   │   ├── __init__.py
│   │   │   ├── openai_generator.py
│   │   │   ├── code_generator.py
│   │   │   └── test_generator.py
│   │   ├── quality/
│   │   │   ├── __init__.py
│   │   │   ├── validator.py
│   │   │   ├── linter.py
│   │   │   └── test_runner.py
│   │   └── templates/
│   │       ├── learning_path.md.j2
│   │       ├── assignment.py.j2
│   │       ├── starter_example.py.j2
│   │       └── test_template.py.j2
├── tests/
├── config/
│   ├── topic_schemas/
│   └── default_topics.json
├── requirements.txt
├── setup.py
├── pyproject.toml
└── README.md
```