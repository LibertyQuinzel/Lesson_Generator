from __future__ import annotations

from pathlib import Path
from click.testing import CliRunner

from lesson_generator.cli.main import main


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def test_cli_short_flag_beginner_scales_time(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "create",
            "My Fancy Topic",
            "--output",
            str(tmp_path),
            "--no-ai",
            "-b",
        ],
    )
    assert result.exit_code == 0, result.output
    # Directory name should be normalized (snake-ish lower)
    # Find the single created topic directory
    topics = [p for p in tmp_path.iterdir() if p.is_dir()]
    assert len(topics) == 1
    topic_dir = topics[0]

    # Module 1 README should show beginner-scaled estimated time: base 60 -> 48
    mod1 = topic_dir / "module_1_basics" / "README.md"
    content = _read_text(mod1)
    assert "Estimated Time: 48 minutes" in content


def test_cli_short_flag_advanced_scales_time(tmp_path: Path):
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "create",
            "Another Topic",
            "--output",
            str(tmp_path),
            "--no-ai",
            "-a",
        ],
    )
    assert result.exit_code == 0, result.output
    topics = [p for p in tmp_path.iterdir() if p.is_dir()]
    # This run creates another topic; find the most recent dir containing module_1_basics
    topic_dir = max(topics, key=lambda p: p.stat().st_mtime)
    mod1 = topic_dir / "module_1_basics" / "README.md"
    content = _read_text(mod1)
    # Advanced scaling base 60 -> 78
    assert "Estimated Time: 78 minutes" in content
