# Lesson Generator

AI-powered lesson generator for programming courses that creates comprehensive, structured lessons based on topics. Built with robust error handling, type safety, and extensive testing.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Virtual environment tool (venv recommended)
- Git (for installation from source)
- OpenAI API key (optional, for AI-powered generation)

### Installation

```bash
# 1. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install from source (recommended for latest features)
git clone https://github.com/LibertyQuinzel/lesson-generator.git
cd lesson-generator
pip install -r requirements.txt
pip install -e .

# Optional: Install development dependencies
pip install -r requirements-dev.txt
```

### Development Setup

For contributors and developers:
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
pylint src/lesson_generator

# Generate documentation
pdoc --html --output-dir docs src/lesson_generator
```

### Basic Usage

```bash
# 1. Basic lesson generation
lesson-generator create "defensive programming" --modules 2

# 2. Multiple lessons with specific configuration
lesson-generator create \
    "defensive programming" \
    "error handling" \
    "iterators" \
    --modules 2 \
    --difficulty intermediate \
    --output ./my_lessons

# 3. AI-powered generation (requires OpenAI API key)
export OPENAI_API_KEY="your-key-here"
lesson-generator create "advanced algorithms" \
    --strict-ai \
    --modules 3 \
    --difficulty advanced

# 4. Offline/fallback mode (no API key needed)
lesson-generator create "basic python" \
    --no-ai \
    --modules 2 \
    --difficulty beginner
```

### Error Handling & Validation

The generator includes comprehensive error handling:

1. **Input Validation**
   - Topic/module names are automatically sanitized
   - Invalid configurations are caught early
   - Helpful error messages guide correction

2. **Graceful Fallbacks**
   - AI generation failures fall back to deterministic content
   - File system errors are handled safely
   - Network issues won't crash the generator

3. **Error Reporting**
   - Detailed logs in `errors.txt` per topic
   - Clear error messages with context
   - Stack traces for development debugging

## Command Reference

### Getting Help

```bash
# View all commands
lesson-generator --help

# Get detailed help for specific command
lesson-generator create --help

# See version information
lesson-generator --version
```

### Core Options

#### Output Control
```bash
--output PATH          # Output directory (default: ./generated_lessons)
--modules N           # Modules per lesson (default: 5)
--workers N          # Parallel processing threads (default: 1)
```

#### Difficulty Settings
```bash
--difficulty LEVEL    # Set complexity: beginner|intermediate|advanced
-b                   # Shortcut for --difficulty beginner
-i                   # Shortcut for --difficulty intermediate
-a                   # Shortcut for --difficulty advanced
```

#### Content Generation
```bash
--strict-ai          # Require AI generation (default)
--no-strict-ai      # Allow fallback content
--no-ai             # Force deterministic content
--openai-api-key KEY # Set API key (or use env var)
```

#### Template Customization
```bash
--templates DIR      # Override built-in templates
--reference DIR     # Extract templates from reference
--cache/--no-cache  # Enable/disable generation cache
```

### Troubleshooting Guide

1. **AI Generation Issues**
   - Error: "OpenAI API key not found"
     ```bash
     export OPENAI_API_KEY="your-key"
     # or
     lesson-generator create ... --openai-api-key "your-key"
     ```
   - Error: "AI generation failed"
     ```bash
     # Try with fallbacks enabled
     lesson-generator create ... --no-strict-ai
     ```

2. **File System Issues**
   - Error: "Permission denied"
     ```bash
     # Check directory permissions
     sudo chown -R $USER:$USER ./generated_lessons
     ```
   - Error: "Directory not empty"
     ```bash
     # Use a clean output directory
     lesson-generator create ... --output ./new_lessons
     ```

3. **Debug Logging**
   - Check `errors.txt` in topic directory
   - Run with increased verbosity:
     ```bash
     lesson-generator create ... --verbose
     ```

### Environment Setup

1. **Set OpenAI API Key:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   # Or create .env file
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

2. **Configure Python Environment:**
   ```bash
   python -m venv lesson_gen_env
   source lesson_gen_env/bin/activate  # Linux/Mac
   pip install lesson-generator
   ```

## 📚 Features

 - **Strict AI Mode**: Use `--strict-ai/--no-strict-ai` to require AI for all content (on by default)
 - **Difficulty-aware generation**: `--difficulty` affects not only estimated times but also the breadth/complexity of starter examples and assignments (keeps APIs simple; scales method count and minor edge cases).
 - **Input sanitation**: Topic/module names can be provided as free-form text; the generator normalizes them to safe snake_case internally. You don’t need to pre-format names.

## ✅ GitHub-ready output

Every generated lesson includes:

- Root files: `README.md`, `requirements.txt`, `pytest.ini`, `Makefile`, `setup.cfg`, `.gitignore`
- Per-module content: `README.md` (learning path), `starter_example.py`, `assignment_a.py` (+ `assignment_b.py` for assignment/project modules), `test_*` files, and `extra_exercises.md`
- CI: A GitHub Actions workflow at `.github/workflows/python-tests.yml` that installs deps and runs `pytest` on push and pull requests

You can customize or remove these by editing the templates under `src/lesson_generator/templates` or passing `--templates DIR` to override.

## 🏗️ Project Architecture

### Code Quality Standards

1. **Error Handling**
   - Specific exception types for different error categories
   - Graceful fallbacks for AI and file system operations
   - Detailed error messages with context
   - Proper exception chaining with `raise ... from`

2. **Type Safety**
   - Comprehensive type hints throughout
   - Runtime type checking for critical operations
   - Clear interface definitions
   - MyPy validation in CI

3. **Testing**
   - 100% code coverage requirement
   - Unit tests for all components
   - Integration tests for full workflows
   - Property-based testing for complex operations

4. **Documentation**
   - Google-style docstrings
   - Clear function/class responsibilities
   - Usage examples in docstrings
   - Up-to-date architecture docs

### Project Structure

```
lesson_generator/
├── src/
│   └── lesson_generator/
│       ├── cli/           # Command line interface
│       ├── core/          # Core generation logic
│       ├── content/       # Content generation (AI/fallback)
│       └── templates/     # Jinja2 templates
├── tests/
│   ├── unit/             # Unit tests
│   └── integration/      # Integration tests
├── docs/                 # Documentation
└── examples/            # Example lessons
```

### Key Components

1. **Core Engine** (`core/`)
   - Generator orchestration
   - File system management
   - Template processing
   - Error handling

2. **Content Generation** (`content/`)
   - OpenAI integration
   - Fallback generation
   - Content caching
   - Template extraction

3. **CLI Interface** (`cli/`)
   - Command parsing
   - Configuration management
   - Progress reporting
   - Error display

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system design.

## 🧪 Testing Strategy

See [TDD_STRATEGY.md](TDD_STRATEGY.md) for testing approach and guidelines.

## 📋 Development Plan

See [SPRINT_PLAN.md](SPRINT_PLAN.md) for development roadmap and sprint details.

## 🔒 Security

See [docs/SECURITY.md](docs/SECURITY.md) for safeguards, reporting, and our threat model.

## ⚡ Performance
   --openai-api-key your_api_key \
   --strict-ai  # ensure all files are AI-generated and fallbacks are disabled
See [docs/PERFORMANCE.md](docs/PERFORMANCE.md) for benchmarking guidance and tips.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Developer tasks

Optional convenience Makefile targets are included for this repository (not the generated lessons):

```bash
make install     # install dependencies
make fmt         # format with black
make lint        # pylint the src tree (non-fatal)
make typecheck   # mypy type checking (non-fatal)
make test        # run unit tests
make coverage    # run tests with coverage (fails if < 97%)
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Documentation](https://lesson-generator.readthedocs.io)
- [PyPI Package](https://pypi.org/project/lesson-generator/)
- [GitHub Repository](https://github.com/LibertyQuinzel/lesson-generator)
- [Issue Tracker](https://github.com/LibertyQuinzel/lesson-generator/issues)