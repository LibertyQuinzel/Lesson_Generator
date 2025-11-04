# Security Policy

This project generates code and documentation from templates and AI content. To minimize risk, we apply the following safeguards by default:

- No dynamic evaluation: Generated code is validated to forbid `exec` and `eval`.
- Forbidden imports: `os`, `subprocess`, `shlex`, `socket`, and `requests` are disallowed in generated Python to avoid unintended system or network access.
- AST validation: Every generated Python file is parsed with `ast.parse()` and compiled to bytecode to catch syntax errors early.
- Template hardening: Jinja2 autoescape is disabled for Python files to prevent accidental escaping, and templates include defensive guards for `None`/empty values.
- Content normalization: AI outputs are parsed as JSON and sanitized; we fall back to a deterministic content generator if parsing fails.
- Rate limiting and retries: External API calls are retried with backoff and gracefully fall back when unavailable.

## Reporting a Vulnerability

If you discover a security-related issue, please do not open a public issue. Instead, email the maintainers or use your organization’s private reporting channel. Provide:

- A minimal reproduction and version info
- Potential impact and suggested mitigations
- Any logs or outputs that help investigation

We aim to acknowledge within 72 hours and provide a mitigation or fix as soon as feasible.

## Supply Chain and Dependencies

- Dependencies are pinned via `pyproject.toml`/`requirements.txt` in CI.
- CI builds packages and runs `twine check` to verify valid distribution artifacts.
- Linting and type-checks (Black, isort, Flake8, Pylint, mypy) run on every PR.

## Configuration Hardening

- Users can provide custom templates. Generated Python still undergoes AST checks.
- Difficulty scaling affects only estimated times; it does not change code safety checks.
- Caching only stores content prompts/responses by a deterministic key.

## Threat Model (high level)

- Primary: Malicious or unsafe code in generated outputs.
- Secondary: Template injection or poorly formed prompt output leading to invalid files.
- Mitigations: AST/compile validation, forbidden imports, no dynamic eval, strict JSON parsing with fallback.
