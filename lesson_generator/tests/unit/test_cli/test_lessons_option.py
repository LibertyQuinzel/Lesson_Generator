from __future__ import annotations

from click.testing import CliRunner

from lesson_generator.cli.main import main


def test_cli_limits_number_of_lessons_with_flag(tmp_path):
    runner = CliRunner()
    # Provide three topics but request only two lessons
    result = runner.invoke(
        main,
        [
            "create",
            "topicone",
            "topictwo",
            "topicthree",
            "--lessons",
            "2",
            "--output",
            str(tmp_path),
            "--dry-run",
        ],
    )
    assert result.exit_code == 0
    out = result.output
    # Should include the first two topic names but not the third
    assert "topicone" in out
    assert "topictwo" in out
    assert "topicthree" not in out
