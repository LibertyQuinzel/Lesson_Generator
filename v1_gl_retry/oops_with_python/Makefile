.PHONY: help install test test-cov test-fast lint format clean docs check-all setup-dev
.DEFAULT_GOAL := help

# Colors for output
YELLOW := \033[1;33m
GREEN := \033[1;32m
RED := \033[1;31m
BLUE := \033[1;34m
NC := \033[0m # No Color

# Python and pip commands
PYTHON := python3
PIP := pip3

help: ## Show this help message
	@echo "$(BLUE)Defensive Programming Course - Development Commands$(NC)"
	@echo ""
	@echo "$(YELLOW)Setup Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(setup|install)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Testing Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(test)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Code Quality Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -E "(lint|format|check)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)Other Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -vE "(setup|install|test|lint|format|check)" | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'

setup-dev: ## Set up development environment with virtual environment
	@echo "$(YELLOW)Setting up development environment...$(NC)"
	@if [ ! -d "venv" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv venv; \
	fi
	@echo "Activating virtual environment and installing dependencies..."
	@. venv/bin/activate && $(PIP) install --upgrade pip
	@. venv/bin/activate && $(PIP) install -r requirements.txt
	@echo "$(GREEN)Development environment setup complete!$(NC)"
	@echo "$(BLUE)To activate: source venv/bin/activate$(NC)"

install: ## Install dependencies in current environment
	@echo "$(YELLOW)Installing dependencies...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "$(GREEN)Dependencies installed successfully!$(NC)"

test: ## Run all tests with coverage
	@echo "$(YELLOW)Running all tests with coverage...$(NC)"
	pytest --cov --cov-report=term-missing --cov-report=html

test-fast: ## Run tests without coverage (faster)
	@echo "$(YELLOW)Running tests (fast mode)...$(NC)"
	pytest --tb=short

test-cov: ## Run tests with detailed coverage report
	@echo "$(YELLOW)Running tests with detailed coverage...$(NC)"
	pytest --cov --cov-report=term-missing --cov-report=html --cov-report=xml
	@echo "$(BLUE)Coverage report generated in htmlcov/index.html$(NC)"

test-module1: ## Run tests for Module 1 (EAFP vs LBYL)
	@echo "$(YELLOW)Running Module 1 tests...$(NC)"
	pytest module_1_eafp_vs_lbyl/ -v

test-module2: ## Run tests for Module 2 (Invariants & Assertions)
	@echo "$(YELLOW)Running Module 2 tests...$(NC)"
	pytest module_2_invariants_assertions/ -v

test-module3: ## Run tests for Module 3 (Exception Hierarchy)
	@echo "$(YELLOW)Running Module 3 tests...$(NC)"
	pytest module_3_exceptions_hierarchy/ -v

test-module4: ## Run tests for Module 4 (Design by Contract)
	@echo "$(YELLOW)Running Module 4 tests...$(NC)"
	pytest module_4_design_by_contract/ -v

test-module5: ## Run tests for Module 5 (Sentinel Values & Logging)
	@echo "$(YELLOW)Running Module 5 tests...$(NC)"
	pytest module_5_sentinel_values_logging/ -v

test-assignments: ## Run only assignment tests
	@echo "$(YELLOW)Running assignment tests...$(NC)"
	pytest -k "assignment" -v

test-debug: ## Run tests with debugging output
	@echo "$(YELLOW)Running tests in debug mode...$(NC)"
	pytest -v -s --tb=long

lint: ## Run pylint on all Python files
	@echo "$(YELLOW)Running pylint...$(NC)"
	pylint module_*/*.py || true
	@echo "$(GREEN)Linting complete!$(NC)"

lint-module1: ## Run pylint on Module 1
	@echo "$(YELLOW)Linting Module 1...$(NC)"
	pylint module_1_eafp_vs_lbyl/*.py

lint-module2: ## Run pylint on Module 2
	@echo "$(YELLOW)Linting Module 2...$(NC)"
	pylint module_2_invariants_assertions/*.py

lint-module3: ## Run pylint on Module 3
	@echo "$(YELLOW)Linting Module 3...$(NC)"
	pylint module_3_exceptions_hierarchy/*.py

lint-module4: ## Run pylint on Module 4
	@echo "$(YELLOW)Linting Module 4...$(NC)"
	pylint module_4_design_by_contract/*.py

lint-module5: ## Run pylint on Module 5
	@echo "$(YELLOW)Linting Module 5...$(NC)"
	pylint module_5_sentinel_values_logging/*.py

format: ## Auto-format code with black
	@echo "$(YELLOW)Formatting code with black...$(NC)"
	black module_*/*.py
	@echo "$(GREEN)Code formatting complete!$(NC)"

format-check: ## Check if code formatting is correct
	@echo "$(YELLOW)Checking code formatting...$(NC)"
	black --check module_*/*.py

check-all: ## Run all quality checks (tests, linting, formatting)
	@echo "$(YELLOW)Running all quality checks...$(NC)"
	@echo "$(BLUE)1. Checking code formatting...$(NC)"
	@black --check module_*/*.py || (echo "$(RED)Code formatting issues found. Run 'make format' to fix.$(NC)" && exit 1)
	@echo "$(BLUE)2. Running linting...$(NC)"
	@pylint module_*/*.py --fail-under=8.0 || (echo "$(RED)Linting issues found. Fix issues or adjust pylint score.$(NC)" && exit 1)
	@echo "$(BLUE)3. Running tests with coverage...$(NC)"
	@pytest --cov --cov-fail-under=80 || (echo "$(RED)Tests failed or coverage too low.$(NC)" && exit 1)
	@echo "$(GREEN)All quality checks passed!$(NC)"

clean: ## Clean up generated files
	@echo "$(YELLOW)Cleaning up generated files...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.orig" -delete 2>/dev/null || true
	rm -rf htmlcov/ 2>/dev/null || true
	rm -rf .coverage 2>/dev/null || true
	rm -rf coverage.xml 2>/dev/null || true
	rm -rf dist/ 2>/dev/null || true
	rm -rf build/ 2>/dev/null || true
	rm -rf *.egg-info/ 2>/dev/null || true
	@echo "$(GREEN)Cleanup complete!$(NC)"

docs: ## Generate documentation (placeholder)
	@echo "$(YELLOW)Documentation generation not yet implemented$(NC)"
	@echo "$(BLUE)See README.md and individual module learning_path.md files$(NC)"

profile-tests: ## Run tests with profiling
	@echo "$(YELLOW)Running tests with profiling...$(NC)"
	pytest --profile --profile-svg

quick-check: ## Quick development check (fast tests + basic linting)
	@echo "$(YELLOW)Running quick development checks...$(NC)"
	@echo "$(BLUE)1. Fast tests...$(NC)"
	@pytest --tb=short -x
	@echo "$(BLUE)2. Basic linting (errors only)...$(NC)"
	@pylint module_*/*.py --errors-only
	@echo "$(GREEN)Quick check complete!$(NC)"

# CI/CD related commands
ci-install: ## Install dependencies for CI environment
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

ci-test: ## Run tests in CI environment
	pytest --cov --cov-report=xml --cov-report=term --junitxml=test-results.xml

ci-quality: ## Run quality checks for CI
	pylint module_*/*.py --output-format=parseable --reports=no --score=no > pylint-report.txt || true
	black --check module_*/*.py

# Development shortcuts
dev: test-fast lint-errors ## Quick development cycle (fast tests + error-only linting)

lint-errors: ## Run pylint showing only errors
	@echo "$(YELLOW)Running pylint (errors only)...$(NC)"
	pylint module_*/*.py --errors-only || true

watch-tests: ## Watch files and run tests on changes (requires inotify-tools)
	@echo "$(YELLOW)Watching for file changes and running tests...$(NC)"
	@echo "$(BLUE)Press Ctrl+C to stop$(NC)"
	@while inotifywait -r -e modify module_*/; do \
		echo "$(YELLOW)Files changed, running tests...$(NC)"; \
		make test-fast; \
		echo "$(GREEN)Waiting for changes...$(NC)"; \
	done

# Verify installation
verify: ## Verify installation and setup
	@echo "$(YELLOW)Verifying installation...$(NC)"
	@$(PYTHON) --version
	@$(PIP) --version
	@pytest --version
	@pylint --version
	@echo "$(GREEN)Installation verified!$(NC)"
	@echo "$(BLUE)Ready to start learning defensive programming!$(NC)"