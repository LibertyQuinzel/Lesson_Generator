# Development Makefile for lesson_generator package

.PHONY: install fmt lint test coverage typecheck all

install:
	python -m pip install -r requirements.txt

fmt:
	black src tests

lint:
	pylint -j 0 src || true

# Type checking (optional)
typecheck:
	mypy --config-file mypy.ini src || true

# Run unit tests
test:
	pytest -q

# Coverage with a high bar; adjust as needed
coverage:
	pytest --maxfail=1 --disable-warnings --cov=lesson_generator --cov-report=term-missing --cov-report=html --cov-fail-under=97

all: fmt lint typecheck test coverage
