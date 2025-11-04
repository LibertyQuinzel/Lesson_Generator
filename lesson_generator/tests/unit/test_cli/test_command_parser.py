from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from lesson_generator.cli.main import main


def test_cli_shows_usage_without_args():
    runner = CliRunner()
    result = runner.invoke(main, ["create"])  # missing topics/config
    assert result.exit_code != 0
    assert "Provide at least one TOPIC" in result.output


def test_cli_accepts_topics_and_dry_run(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(main, [
        "create",
        "async_programming",
        "--output",
        str(tmp_path),
        "--dry-run",
    ])
    assert result.exit_code == 0
    assert "Lesson Generation Summary" in result.output
