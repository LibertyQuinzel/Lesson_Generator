from lesson_generator.core.generator import LessonGenerator
import pytest


def test_validate_python_syntax_allows_simple_code():
    LessonGenerator._validate_python_syntax("def f():\n    return 1\n", "X.py")


def test_validate_python_syntax_forbids_eval():
    with pytest.raises(ValueError):
        LessonGenerator._validate_python_syntax("def f():\n    return eval('1')\n", "X.py")


def test_validate_python_syntax_forbids_os_import():
    with pytest.raises(ValueError):
        LessonGenerator._validate_python_syntax("import os\nprint('x')\n", "X.py")
