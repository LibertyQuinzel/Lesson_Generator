# Contributing to Lesson Generator

Thank you for your interest in contributing to Lesson Generator! This document provides guidelines and standards for contributing to the project.

## Development Setup

1. **Clone and Install**
   ```bash
   git clone https://github.com/LibertyQuinzel/lesson-generator.git
   cd lesson-generator
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   pip install -e .
   ```

2. **Run Tests**
   ```bash
   pytest                # Run all tests
   pytest -v            # Verbose output
   pytest --cov=src     # Coverage report
   ```

3. **Code Quality**
   ```bash
   pylint src/lesson_generator  # Linting
   black src/                   # Code formatting
   mypy src/                   # Type checking
   ```

## Code Standards

1. **Type Hints**
   - All functions must include return type annotations
   - Use Optional[] for nullable parameters
   - Add typing.Protocol for interfaces
   - Document type variables in generics

2. **Error Handling**
   - Use specific exception types
   - Include context in error messages
   - Implement proper exception chaining
   - Document exceptions in docstrings

3. **Documentation**
   - Follow Google docstring style
   - Include usage examples
   - Document all parameters
   - List raised exceptions

4. **Testing**
   - Maintain 100% coverage
   - Include edge cases
   - Mock external services
   - Use meaningful test names

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Update documentation
5. Run full test suite
6. Submit PR with description

## Best Practices

1. **Code Organization**
   - Keep functions focused and small
   - Use clear, descriptive names
   - Follow SOLID principles
   - Maintain separation of concerns

2. **Performance**
   - Profile code changes
   - Use appropriate data structures
   - Implement caching where beneficial
   - Consider memory usage

3. **Security**
   - Validate all inputs
   - Sanitize file paths
   - Handle secrets securely
   - Use safe defaults

4. **Maintainability**
   - Write self-documenting code
   - Keep complexity low
   - Add meaningful comments
   - Use consistent style