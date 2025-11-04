"""CLI entrypoint for lesson-generator."""
from __future__ import annotations

import json
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.panel import Panel
from rich.table import Table

from lesson_generator.core.generator import LessonGenerator, GenerationOptions
from lesson_generator.content import ContentGenerator

# Load environment variables from a local .env file if present
try:  # lightweight optional dependency usage
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    # If python-dotenv isn't available or any issue occurs, continue without it.
    # OPENAI_API_KEY can still be provided via the environment or CLI flag.
    pass


console = Console()


def _discover_default_reference_dir() -> Optional[Path]:
    """Best-effort discovery of a reference course folder.

    Heuristics:
    - Respect LESSON_GENERATOR_REFERENCE_DIR if it points to an existing directory
    - Look for a sibling folder next to the project root that contains module_1_* dirs
    - Try common names from current working directory as well
    Returns a Path if found, else None.
    """
    # 1) Environment variable override
    try:
        import os

        env_path = os.getenv("LESSON_GENERATOR_REFERENCE_DIR")
        if env_path:
            p = Path(env_path).expanduser().resolve()
            if p.exists() and p.is_dir():
                return p
    except Exception:
        pass

    # 2) Try sibling folders relative to project root: only 'reference_lesson'
    try:
        here = Path(__file__).resolve()
        # src/lesson_generator/cli/main.py -> project root two levels up from src
        project_root = here.parents[3]
        candidates = [
            project_root / "reference_lesson",
            Path.cwd() / "reference_lesson",
        ]
        for cand in candidates:
            if cand.exists() and cand.is_dir():
                # Looks like a reference course if it has a README or module_1_* folder
                has_module = any(p.is_dir() for p in cand.glob("module_1_*/"))
                has_readme = (cand / "README.md").exists()
                if has_module or has_readme:
                    return cand
    except Exception:
        pass

    return None


@click.group(help="AI-powered lesson generator.")
def main() -> None:  # pragma: no cover - exercised via Click runner
    """Root command group."""
    pass


@main.command(name="create", help="Create lessons for given topics or a config file.")
@click.argument("topics", nargs=-1)
@click.option(
    "--config",
    "config_path",
    type=click.Path(path_type=Path, exists=True, dir_okay=False),
    help="Path to a JSON file with topic definitions (array or single object).",
)
@click.option(
    "--output",
    "output_dir",
    type=click.Path(path_type=Path, file_okay=False, resolve_path=True),
    default=Path("generated_lessons"),
    show_default=True,
    help="Directory where lessons will be created.",
)
@click.option(
    "--modules",
    "modules_per_lesson",
    type=click.IntRange(min=1, max=10),
    default=5,
    show_default=True,
    help="Number of modules per lesson.",
)
@click.option("--dry-run", is_flag=True, help="Show what would be created without writing files.")
@click.option(
    "--openai-api-key",
    "openai_api_key",
    type=str,
    default=None,
    help="OpenAI API key (fallback to OPENAI_API_KEY env var).",
)
@click.option(
    "--no-ai",
    is_flag=True,
    help="Do not use OpenAI; generate deterministic content instead.",
)
@click.option(
    "--strict-ai/--no-strict-ai",
    "strict_ai",
    default=True,
    show_default=True,
    help="Require AI for all generated content (disable internal fallbacks).",
)
@click.option(
    "--workers",
    type=click.IntRange(min=1, max=16),
    default=1,
    show_default=True,
    help="Parallel workers for generating multiple topics.",
)
@click.option(
    "--templates",
    "templates_dir",
    type=click.Path(path_type=Path, exists=True, file_okay=False),
    default=None,
    help="Custom templates directory to override built-in templates.",
)
@click.option(
    "--reference",
    "reference_dir",
    type=click.Path(path_type=Path, exists=True, file_okay=False),
    default=None,
    help="Reference lesson folder to extract templates from before generation.",
)
@click.option(
    "--difficulty",
    type=click.Choice(["beginner", "intermediate", "advanced"], case_sensitive=False),
    default=None,
    help="Override difficulty for all topics (affects estimated times).",
)
@click.option("-b", "diff_beginner", is_flag=True, help="Shortcut: set difficulty=beginner")
@click.option("-i", "diff_intermediate", is_flag=True, help="Shortcut: set difficulty=intermediate")
@click.option("-a", "diff_advanced", is_flag=True, help="Shortcut: set difficulty=advanced")
@click.option(
    "--cache/--no-cache",
    "use_cache",
    default=True,
    show_default=True,
    help="Enable caching for repeated content generation calls.",
)
@click.option(
    "--lessons",
    "lessons_count",
    type=click.IntRange(min=1, max=100),
    default=1,
    show_default=True,
    help="Number of lessons to generate (limits how many topics are processed).",
)
def create_cmd(
    topics: List[str],
    config_path: Optional[Path],
    output_dir: Path,
    modules_per_lesson: Optional[int],
    dry_run: bool,
    openai_api_key: Optional[str],
    no_ai: bool,
    strict_ai: bool,
    workers: Optional[int] = 1,
    templates_dir: Optional[Path] = None,
    difficulty: Optional[str] = None,
    diff_beginner: bool = False,
    diff_intermediate: bool = False,
    diff_advanced: bool = False,
    use_cache: bool = True,
    reference_dir: Optional[Path] = None,
    lessons_count: int = 1,
) -> None:
    """Create lessons from topics or a configuration file."""
    if not topics and not config_path:
        raise click.UsageError("Provide at least one TOPIC or --config pointing to a topic JSON file.")

    # Reconcile difficulty from short flags vs explicit option
    short_flags = sum([1 if diff_beginner else 0, 1 if diff_intermediate else 0, 1 if diff_advanced else 0])
    if difficulty and short_flags:
        raise click.UsageError("Provide either --difficulty or one of -b/-i/-a, not both.")
    if not difficulty and short_flags:
        difficulty = "beginner" if diff_beginner else ("intermediate" if diff_intermediate else "advanced")

    generation_options = GenerationOptions(
        output_dir=output_dir,
        modules_override=modules_per_lesson,
        dry_run=dry_run,
        workers=workers,
        difficulty_override=(difficulty.lower() if difficulty else None),
        strict_ai_only=strict_ai,
        lessons_count=lessons_count,
    # ai_direct_code is always enabled by default in GenerationOptions
    )

    # Choose content generator
    content_gen: ContentGenerator | None = None
    if no_ai:
        content_gen = None
    else:
        try:
            from lesson_generator.content.openai_generator import OpenAIContentGenerator

            content_gen = OpenAIContentGenerator(api_key=openai_api_key, allow_fallbacks=not strict_ai)
        except Exception:
            content_gen = None

    # Enforce AI-only generation when strict_ai is enabled
    if strict_ai and not no_ai and content_gen is None:
        raise click.ClickException(
            "Strict AI mode is enabled but an AI content generator is not available. "
            "Ensure the 'openai' package is installed and OPENAI_API_KEY is set, or run with --no-strict-ai or --no-ai."
        )

    # Optional caching wrapper
    if use_cache:
        try:
            from lesson_generator.content import CachedContentGenerator  # type: ignore

            content_gen = CachedContentGenerator(content_gen)
        except Exception:
            pass

    # If a reference folder is provided (or discovered), extract templates to a temp dir first
    extracted_templates_dir: Optional[Path] = None
    # Discover default reference directory if not explicitly provided
    if reference_dir is None:
        reference_dir = _discover_default_reference_dir()

    if reference_dir is not None:
        try:
            from lesson_generator.core.template_extractor import extract_to_temp

            extracted_templates_dir = extract_to_temp(reference_dir)
        except Exception as exc:  # pragma: no cover - defensive
            raise click.ClickException(f"Failed to extract templates from reference: {exc}") from exc

    # Final templates directory precedence: explicit --templates > extracted > built-in
    effective_templates = templates_dir or extracted_templates_dir

    generator = LessonGenerator(templates_dir=effective_templates, content_generator=content_gen)

    # Load from config if provided
    topics_payload: Optional[str] = None
    if config_path:
        try:
            topics_payload = config_path.read_text(encoding="utf-8")
        except OSError as exc:
            raise click.FileError(str(config_path), hint=str(exc)) from exc

    # Determine total items for progress (best-effort)
    total_count = 0
    if topics:
        total_count += len(topics)
    if topics_payload:
        try:
            data = json.loads(topics_payload)
            total_count += len(data) if isinstance(data, list) else 1
        except Exception:
            # If payload can't be parsed here, generator will handle/raise; keep progress simple.
            pass
    # Apply the lessons limit for progress estimation
    if total_count > 0 and lessons_count:
        total_count = min(total_count, lessons_count)

    def _progress_cb(item, idx, total):  # noqa: ANN001 - runtime callback
        if task_id is not None:
            progress.advance(task_id)
            progress.refresh()

    # Detailed per-module progress tracking
    # key: (topic_name, module_index) -> {task_id, completed, seen}
    module_tasks: dict[tuple[str, int], dict] = {}
    STEP_MAX = 8  # approximate number of generation steps per module

    def _module_cb(topic_name: str, module_index: int, module_total: int, module_name: str, step: str) -> None:
        if progress is None:
            return
        key = (topic_name, module_index)
        state = module_tasks.get(key)
        if state is None:
            # Create a new task for this module
            desc = f"[{topic_name}] module {module_index}/{module_total}: {module_name}"
            tid = progress.add_task(desc, total=STEP_MAX)
            state = {"task_id": tid, "completed": 0, "seen": set()}
            module_tasks[key] = state
        # Normalize step and count unique steps
        st = (step or "").strip().lower()
        if st == "start" and state["completed"] == 0:
            progress.advance(state["task_id"], 1)
            state["completed"] = 1
            state["seen"].add(st)
            return
        if st and st not in state["seen"] and st != "done":
            state["seen"].add(st)
            state["completed"] += 1
            progress.advance(state["task_id"], 1)
            # Update description to reflect current step
            desc = f"[{topic_name}] module {module_index}/{module_total}: {module_name} - {st}"
            progress.update(state["task_id"], description=desc)
            return
        if st == "done":
            # Complete the task
            remaining = STEP_MAX - state["completed"]
            if remaining > 0:
                progress.advance(state["task_id"], remaining)
            desc = f"[{topic_name}] module {module_index}/{module_total}: {module_name} - done"
            progress.update(state["task_id"], description=desc)

    progress = None
    task_id = None
    result = None
    if total_count > 0 and not dry_run:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("{task.completed}/{task.total}"),
            TimeElapsedColumn(),
            transient=True,
            console=console,
        ) as progress:
            task_id = progress.add_task("Generating lessons", total=total_count)
            result = generator.generate(
                topics=topics,
                topics_json=topics_payload,
                options=generation_options,
                on_progress=_progress_cb,
                on_module_progress=_module_cb,
            )
    else:
        result = generator.generate(
            topics=topics,
            topics_json=topics_payload,
            options=generation_options,
            on_module_progress=_module_cb if not dry_run else None,
        )

    table = Table(title="Lesson Generation Summary", show_lines=False)
    table.add_column("Topic", style="bold")
    table.add_column("Status")
    table.add_column("Path")

    for r in result.items:
        table.add_row(r.topic_name, r.status, str(r.output_path or "-"))

    console.print(Panel.fit(table, title="Results", border_style="green"))

    # Do not stop the process with a non-zero exit when errors occur; errors are logged to errors.txt per topic.
    # Keep exit code 0 so long-running generation pipelines can continue.


 # Note: No 'quickstart' subcommand; keep surface minimal. Use --help for guidance.


if __name__ == "__main__":  # pragma: no cover
    main()
