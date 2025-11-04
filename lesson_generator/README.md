# Lesson Generator

AI-powered lesson generator for programming courses that creates comprehensive, structured lessons based on topics.

## 🚀 Quick Start

### Installation

```bash
# Install from PyPI (when published)
pip install lesson-generator

# Or install from source
git clone https://github.com/LibertyQuinzel/lesson-generator.git
cd lesson-generator
pip install -e .
```

### Basic Usage

```bash
# Generate a single lesson
lesson-generator create async_programming --output ./lessons

# Generate multiple lessons
lesson-generator create async_programming design_patterns testing_strategies --output ./lessons

# Use configuration file
lesson-generator create --config topics.json --output ./lessons

# Advanced options
lesson-generator create async_programming \
    --difficulty intermediate \
    --modules 5 \
    --output ./lessons \
    --openai-api-key your_api_key
```

## Help

Get command help and options at any time:

```bash
# Top-level help
lesson-generator --help

# Help for the 'create' command
lesson-generator create --help
```

Common options (create):
- `--output PATH`           Output directory for generated lessons (default: ./generated_lessons)
- `--modules N`             Number of modules per lesson (default: 5)
- `--difficulty LEVEL`      One of: beginner | intermediate | advanced
- `-b | -i | -a`            Shortcuts for `--difficulty` (beginner | intermediate | advanced)
- `--no-ai`                 Use deterministic content (no API key required)
- `--openai-api-key KEY`    API key (or set env var OPENAI_API_KEY)
- `--strict-ai/--no-strict-ai` Require AI only or allow fallbacks (default: strict)
- `--workers N`             Parallel topic processing (default: 1)
- `--templates DIR`         Point to a directory of Jinja2 templates that override built-ins. Any file with the same name replaces the default. Precedence: `--templates` > templates extracted via `--reference` > built-ins.
- `--reference DIR`         Extract templates from a reference lesson before generating
- `--cache/--no-cache`      Turn the generation cache on/off (default: on). When enabled, repeated requests with the same inputs reuse prior results to avoid re-calling AI/fallback generators within a run; useful for iterative tweaks or multi-topic runs. Cache is local to the current process/run and not persisted.

Troubleshooting:
- AI errors with strict mode: run with `--no-strict-ai` or `--no-ai`, or set `OPENAI_API_KEY` and ensure `openai` is installed.
- See per-topic `errors.txt` inside the output topic folder for detailed generation logs.

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