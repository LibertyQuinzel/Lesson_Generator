# Lesson Generator

AI-powered lesson generator that creates comprehensive, structured programming courses. Built with robust error handling, type safety, and extensive testing.

<div align="center">

[![Tests](https://github.com/LibertyQuinzel/Lesson_Generator/workflows/Tests/badge.svg)](https://github.com/LibertyQuinzel/Lesson_Generator/actions)
[![Coverage](https://codecov.io/gh/LibertyQuinzel/Lesson_Generator/branch/master/graph/badge.svg)](https://codecov.io/gh/LibertyQuinzel/Lesson_Generator)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

## ✨ Features

- **AI-Powered Content**: Generates complete lessons using OpenAI, with fallback options
- **Structured Learning**: Creates multi-module courses with progressive difficulty
- **Practice-Ready**: Includes starter examples, assignments, and automated tests
- **GitHub-Ready**: Built-in CI/CD configurations and project structure
- **Highly Configurable**: Customizable templates and generation options
- **Production Quality**: 100% test coverage, type safety, comprehensive docs

## 🚀 Quick Start

```bash
# Install
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install lesson-generator

# Generate a lesson
export OPENAI_API_KEY="your-key-here"  # Optional, for AI generation
lesson-generator create "python iterators" --modules 2 --difficulty intermediate
```

## 📚 Documentation

For detailed documentation, see [lesson_generator/README.md](lesson_generator/README.md).

### Core Features

1. **AI Integration**
   - OpenAI-powered content generation
   - Fallback to deterministic content
   - Content quality validation

2. **Lesson Structure**
   - Progressive module complexity
   - Practical assignments
   - Automated testing
   - Clear learning paths

3. **Developer Tools**
   - GitHub Actions CI
   - pytest integration
   - Code coverage
   - Style enforcement

## 🛠 Project Structure

```
lesson_generator/
├── src/             # Source code
├── tests/           # Test suite
├── docs/            # Documentation
└── examples/        # Example lessons
```

## 🧪 Quality Standards

- 100% test coverage
- Static type checking
- Comprehensive error handling
- Google-style documentation

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](lesson_generator/CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](lesson_generator/LICENSE) for details.

## 🔗 Links

- [PyPI Package](https://pypi.org/project/lesson-generator/)
- [Documentation](https://lesson-generator.readthedocs.io)
- [Issue Tracker](https://github.com/LibertyQuinzel/Lesson_Generator/issues)