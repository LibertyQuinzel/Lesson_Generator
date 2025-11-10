# Defensive Programming in Python

A comprehensive lesson on defensive programming techniques in Python, designed to teach robust software development practices through hands-on examples, assignments, and real-world applications.

## 📚 Course Overview

This course covers five essential defensive programming modules, each building upon the previous to create a complete understanding of error handling, validation, and robust code design in Python. Perfect for intermediate Python developers looking to write more reliable, maintainable code.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Basic understanding of Python syntax and object-oriented programming
- Familiarity with testing concepts (helpful but not required)

### Environment Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd defensive_programming_lesson
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Using venv
   python -m venv defensive_programming_env
   source defensive_programming_env/bin/activate  # Linux/Mac
   # or
   defensive_programming_env\Scripts\activate  # Windows

   # Using conda
   conda create -n defensive_programming python=3.8
   conda activate defensive_programming
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python -m pytest --version
   pylint --version
   ```

5. **Run initial tests to verify setup:**
   ```bash
   pytest --tb=short
   ```

## 📖 Module Structure

Each module follows a consistent learning path designed for progressive skill building:

### [Module 1: EAFP vs LBYL](./module_1_eafp_vs_lbyl/)
**"Easier to Ask for Forgiveness than Permission" vs "Look Before You Leap"**

- **Core Concepts:** Exception handling philosophies, when to use each approach
- **Practical Skills:** Performance implications, code readability, race condition prevention
- **Real-world Applications:** File operations, API calls, concurrent programming
- **Key Files:**
  - [`learning_path.md`](./module_1_eafp_vs_lbyl/learning_path.md) - Complete learning guide
  - [`starter_example.py`](./module_1_eafp_vs_lbyl/starter_example.py) - Introduction examples
  - [`assignment_a.py`](./module_1_eafp_vs_lbyl/assignment_a.py) - Basic assignments
  - [`assignment_b.py`](./module_1_eafp_vs_lbyl/assignment_b.py) - Advanced scenarios
  - [`extra_exercises.md`](./module_1_eafp_vs_lbyl/extra_exercises.md) - 15 additional challenges

### [Module 2: Invariants & Assertions](./module_2_invariants_assertions/)
**Maintaining Code Contracts and Defensive Checks**

- **Core Concepts:** Class invariants, method preconditions/postconditions, assertion strategies
- **Practical Skills:** Debugging with assertions, performance considerations, assertion placement
- **Real-world Applications:** Data validation, algorithm correctness, state management
- **Key Files:**
  - [`learning_path.md`](./module_2_invariants_assertions/learning_path.md) - Comprehensive guide
  - [`starter_example.py`](./module_2_invariants_assertions/starter_example.py) - Invariant examples
  - [`assignment_a.py`](./module_2_invariants_assertions/assignment_a.py) - Class invariants
  - [`assignment_b.py`](./module_2_invariants_assertions/assignment_b.py) - Complex systems
  - [`extra_exercises.md`](./module_2_invariants_assertions/extra_exercises.md) - 15 practice problems

### [Module 3: Exception Hierarchy](./module_3_exceptions_hierarchy/)
**Custom Exceptions and Error Boundary Design**

- **Core Concepts:** Exception inheritance, custom exception design, error boundaries
- **Practical Skills:** Exception chaining, error context preservation, recovery strategies
- **Real-world Applications:** API error handling, system integration, user experience design
- **Key Files:**
  - [`learning_path.md`](./module_3_exceptions_hierarchy/learning_path.md) - Detailed pathway
  - [`starter_example.py`](./module_3_exceptions_hierarchy/starter_example.py) - Exception patterns
  - [`assignment_a.py`](./module_3_exceptions_hierarchy/assignment_a.py) - Custom exceptions
  - [`assignment_b.py`](./module_3_exceptions_hierarchy/assignment_b.py) - Error boundaries
  - [`extra_exercises.md`](./module_3_exceptions_hierarchy/extra_exercises.md) - 15 advanced scenarios

### [Module 4: Design by Contract](./module_4_design_by_contract/)
**Formal Contracts and Specification-Driven Development**

- **Core Concepts:** Preconditions, postconditions, class invariants, contract verification
- **Practical Skills:** Contract-driven design, mathematical verification, formal specifications
- **Real-world Applications:** Financial systems, mathematical libraries, critical software
- **Key Files:**
  - [`learning_path.md`](./module_4_design_by_contract/learning_path.md) - Contract methodology
  - [`starter_example.py`](./module_4_design_by_contract/starter_example.py) - Contract examples
  - [`assignment_a.py`](./module_4_design_by_contract/assignment_a.py) - Basic contracts
  - [`assignment_b.py`](./module_4_design_by_contract/assignment_b.py) - Advanced systems
  - [`extra_exercises.md`](./module_4_design_by_contract/extra_exercises.md) - 15 contract challenges

### [Module 5: Sentinel Values & Logging](./module_5_sentinel_values_logging/)
**Error Signaling Patterns and Observability**

- **Core Concepts:** Sentinel values vs exceptions, logging strategies, observability patterns
- **Practical Skills:** Error signaling design, log level management, debugging techniques
- **Real-world Applications:** Service monitoring, debugging production issues, error reporting
- **Key Files:**
  - [`learning_path.md`](./module_5_sentinel_values_logging/learning_path.md) - Complete guide
  - [`starter_example.py`](./module_5_sentinel_values_logging/starter_example.py) - Pattern examples
  - [`assignment_a.py`](./module_5_sentinel_values_logging/assignment_a.py) - Sentinel patterns
  - [`assignment_b.py`](./module_5_sentinel_values_logging/assignment_b.py) - Logging systems
  - [`extra_exercises.md`](./module_5_sentinel_values_logging/extra_exercises.md) - 15 practical exercises

## 🧪 Testing & Quality Assurance

### Running Tests

```bash
# Run all tests with coverage
pytest --cov --cov-report=html

# Run specific module tests
pytest module_1_eafp_vs_lbyl/ -v

# Run tests with detailed output
pytest --tb=long -v

# Run only failed tests from last run
pytest --lf

# Run tests in parallel (if pytest-xdist installed)
pytest -n auto
```

### Code Quality Checks

```bash
# Run pylint on all modules
pylint module_*/*.py

# Run pylint on specific module
pylint module_1_eafp_vs_lbyl/*.py

# Run with configuration file
pylint --rcfile=.pylintrc module_*/*.py

# Check specific files only
pylint module_1_eafp_vs_lbyl/assignment_a.py
```

### Continuous Integration Setup

The project includes configuration for:
- **pytest**: Comprehensive testing with coverage reporting
- **pylint**: Code quality and style checking
- **GitHub Actions**: Automated testing on multiple Python versions

## 📋 Learning Path Recommendations

### For Beginners to Defensive Programming:
1. Start with Module 1 (EAFP vs LBYL) to understand fundamental philosophies
2. Work through starter examples before attempting assignments
3. Use the learning path guides in each module for structured progression
4. Focus on understanding concepts before optimizing for performance

### For Experienced Python Developers:
1. Review all starter examples to understand the teaching approach
2. Jump directly to Assignment B in each module for challenging scenarios  
3. Explore extra exercises for advanced real-world applications
4. Consider contributing additional examples or improvements

### For Teams/Organizations:
1. Use modules as workshop material (each module = 2-3 hour session)
2. Adapt assignments to reflect your specific domain challenges
3. Create team-specific exercises based on your codebase patterns
4. Establish coding standards based on defensive programming principles

## 🛠️ Development Workflow

### Working on Assignments

1. **Read the learning path:** Each module has a comprehensive guide
2. **Run starter examples:** Understand the concepts with working code
3. **Complete assignments incrementally:** Start with part A, then part B
4. **Run tests frequently:** Use TDD approach when possible
5. **Check code quality:** Run pylint before submitting

### Testing Your Solutions

```bash
# Test specific assignment
pytest module_1_eafp_vs_lbyl/test_assignment_a.py -v

# Test with coverage for specific file
pytest --cov=module_1_eafp_vs_lbyl.assignment_a module_1_eafp_vs_lbyl/test_assignment_a.py

# Debug failing tests
pytest module_1_eafp_vs_lbyl/test_assignment_a.py::test_function_name -v -s
```

## 📊 Assessment Criteria

Each module is evaluated on:
- **Correctness**: All tests pass and requirements are met
- **Defensive Programming**: Proper error handling and validation
- **Code Quality**: Clear, readable, maintainable code
- **Documentation**: Adequate comments and docstrings
- **Testing**: Additional test cases for edge conditions

## 🤝 Contributing

We welcome contributions! Please see areas where you can help:
- Additional real-world examples
- More challenging exercises
- Improved documentation
- Bug fixes and code improvements
- Translation to other languages

## 📚 Additional Resources

- **Books**: "Effective Python" by Brett Slatkin, "Clean Code" by Robert Martin
- **Documentation**: [Python Exception Handling](https://docs.python.org/3/tutorial/errors.html)
- **Tools**: [pytest documentation](https://docs.pytest.org/), [pylint user guide](https://pylint.readthedocs.io/)
- **Standards**: [PEP 8](https://pep8.org/), [PEP 257](https://pep257.readthedocs.io/)

## 🏆 Completion Certificate

Upon completing all modules with passing tests, you'll have demonstrated proficiency in:
- Exception handling strategies and best practices
- Code contract design and implementation
- Error boundary architecture
- Logging and observability patterns
- Defensive programming principles

**Total Learning Time**: 15-20 hours (3-4 hours per module)
**Prerequisites**: Intermediate Python knowledge
**Certification**: Self-assessed through comprehensive test suite