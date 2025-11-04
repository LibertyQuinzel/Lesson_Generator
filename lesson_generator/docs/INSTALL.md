# Installation

## Prerequisites
- Python 3.11+
- pip

## Setup
```bash
# From the lesson_generator folder
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```

## Verify
```bash
pytest -q
```

## Optional
- Set `OPENAI_API_KEY` environment variable to enable AI content generation.
- Use `--no-ai` to stick to deterministic content.
