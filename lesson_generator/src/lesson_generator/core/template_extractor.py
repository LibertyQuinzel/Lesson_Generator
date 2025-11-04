"""Template extraction utilities from a reference lesson folder.

This provides a pragmatic extractor that builds a usable templates directory by
copying the built-in templates and overlaying select files from a reference
lesson. It's designed to get you a working custom templates folder quickly.

Heuristics applied:
- README.md: preserve reference content but replace first heading with
  "# {{ topic.title }}" to keep title dynamic.
- Makefile/setup.cfg: copied as-is into Jinja template filenames.
- Module files: if a reference module_1_* exists, copy files into corresponding
  templates (starter_example.py.j2, assignment.py.j2, learning_path.md.j2,
  test_template.py.j2, test_starter_example.py.j2, extra_exercises.md.j2) when available.
  Note: these copies are static and may not use Jinja variables; they serve as a
  baseline you can edit further.
"""
from __future__ import annotations

from pathlib import Path
import shutil
import tempfile
import re


BUILTIN_TEMPLATE_NAMES = {
    "readme": "readme.md.j2",
    "makefile": "makefile.j2",
    "setup": "setup.cfg.j2",
    "learning_path": "learning_path.md.j2",
    "starter_example": "starter_example.py.j2",
    "assignment": "assignment.py.j2",
    "test_template": "test_template.py.j2",
    "test_starter": "test_starter_example.py.j2",
    "extra": "extra_exercises.md.j2",
}


def _builtin_templates_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "templates"


def _copy_builtins(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    for src in _builtin_templates_dir().glob("*"):
        if src.is_file():
            shutil.copy2(src, dest / src.name)


def _make_readme_template_from_reference(ref_readme: Path, out_file: Path, *, topic_title: str | None = None) -> None:
    text = ref_readme.read_text(encoding="utf-8")
    lines = text.splitlines()
    ref_title = None
    if lines and lines[0].lstrip().startswith("# "):
        ref_title = lines[0].lstrip()[2:].strip()
        lines[0] = "# {{ topic.title }}"
    # Replace obvious occurrences of the reference title with Jinja placeholder
    if topic_title is None:
        topic_title = ref_title
    if topic_title:
        body = "\n".join(lines)
        body = body.replace(topic_title, "{{ topic.title }}")
        # case variants
        body = body.replace(topic_title.upper(), "{{ topic.title|upper }}")
        body = body.replace(topic_title.lower(), "{{ topic.title|lower }}")
        lines = body.splitlines()
    out_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_with_replacements(src: Path, target: Path, *, replacements: dict[str, str] | None = None,
                             regex_subs: list[tuple[re.Pattern[str], str]] | None = None) -> bool:
    try:
        text = src.read_text(encoding="utf-8")
        if replacements:
            for k, v in replacements.items():
                if k:
                    text = text.replace(k, v)
        if regex_subs:
            for pat, repl in regex_subs:
                text = pat.sub(repl, text)
        target.write_text(text, encoding="utf-8")
        return True
    except Exception:
        return False


def extract_templates(reference_dir: Path, output_dir: Path) -> Path:
    """Create a templates directory by combining built-ins and reference files.

    Returns the path to the created templates directory (output_dir).
    """
    reference_dir = reference_dir.resolve()
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1) Start with built-in templates as a safe baseline
    _copy_builtins(output_dir)

    # 2) Overlay with reference files when available
    # Discover reference topic title if present
    readme = reference_dir / "README.md"
    ref_topic_title: str | None = None
    if readme.exists():
        try:
            first = readme.read_text(encoding="utf-8").splitlines()[0]
            if first.lstrip().startswith("# "):
                ref_topic_title = first.lstrip()[2:].strip()
        except Exception:
            ref_topic_title = None
        _make_readme_template_from_reference(readme, output_dir / BUILTIN_TEMPLATE_NAMES["readme"], topic_title=ref_topic_title)

    # Makefile/setup.cfg as-is (content typically doesn't need Jinja variables)
    makefile = reference_dir / "Makefile"
    if makefile.exists():
        _write_with_replacements(makefile, output_dir / BUILTIN_TEMPLATE_NAMES["makefile"])  # simple copy

    setup_cfg = reference_dir / "setup.cfg"
    if setup_cfg.exists():
        _write_with_replacements(setup_cfg, output_dir / BUILTIN_TEMPLATE_NAMES["setup"])  # simple copy

    # 3) Optionally overlay module-specific files from the reference
    # By default we DO NOT override built-in module templates to avoid leaking
    # unrelated reference content (e.g., EAFP/LBYL) into other topics like DRY.
    # Set LESSON_GENERATOR_OVERLAY_MODULE_TEMPLATES=1 to enable overlay.
    import os as _os  # local import to keep module scope minimal
    if _os.getenv("LESSON_GENERATOR_OVERLAY_MODULE_TEMPLATES", "0") not in {"1", "true", "True"}:
        return output_dir

    m1 = None
    for p in sorted(reference_dir.glob("module_1_*")):
        if p.is_dir():
            m1 = p
            break
    if m1 is not None:
        # Compute common replacements from module directory
        module_dir_literal = m1.name
        module_dynamic = "module_{{ module_number }}_{{ module.name }}"
        ref_module_leaf = m1.name.split("module_1_", 1)[1] if "module_1_" in m1.name else m1.name
        replacements: dict[str, str] = {
            module_dir_literal: module_dynamic,
            ref_module_leaf: "{{ module.name }}",
        }
        if ref_topic_title:
            replacements[ref_topic_title] = "{{ topic.title }}"
        regex_subs = [
            (re.compile(r"\b[Mm]odule\s+1\b"), "Module {{ module_number }}"),
            (re.compile(rf"\bmodule_1_{re.escape(ref_module_leaf)}\b"), module_dynamic),
        ]
        # Learning path
        lp = m1 / "learning_path.md"
        if lp.exists():
            _write_with_replacements(lp, output_dir / BUILTIN_TEMPLATE_NAMES["learning_path"],
                                     replacements=replacements, regex_subs=regex_subs)
        # Starter example
        se = m1 / "starter_example.py"
        if se.exists():
            _write_with_replacements(se, output_dir / BUILTIN_TEMPLATE_NAMES["starter_example"],
                                     replacements=replacements, regex_subs=regex_subs)
        # Assignment preference: A if present else B
        asg_a = m1 / "assignment_a.py"
        asg_b = m1 / "assignment_b.py"
        if asg_a.exists():
            _write_with_replacements(asg_a, output_dir / BUILTIN_TEMPLATE_NAMES["assignment"],
                                     replacements=replacements, regex_subs=regex_subs)
        elif asg_b.exists():
            _write_with_replacements(asg_b, output_dir / BUILTIN_TEMPLATE_NAMES["assignment"],
                                     replacements=replacements, regex_subs=regex_subs)
        # Tests
        t_a = m1 / "test_assignment_a.py"
        if t_a.exists():
            _write_with_replacements(t_a, output_dir / BUILTIN_TEMPLATE_NAMES["test_template"],
                                     replacements=replacements, regex_subs=regex_subs)
        ts = m1 / "test_starter_example.py"
        if ts.exists():
            _write_with_replacements(ts, output_dir / BUILTIN_TEMPLATE_NAMES["test_starter"],
                                     replacements=replacements, regex_subs=regex_subs)
        # Extra exercises
        ex = m1 / "extra_exercises.md"
        if ex.exists():
            _write_with_replacements(ex, output_dir / BUILTIN_TEMPLATE_NAMES["extra"],
                                     replacements=replacements, regex_subs=regex_subs)

    return output_dir


def extract_to_temp(reference_dir: Path) -> Path:
    """Extract templates to a temporary directory and return its path."""
    tmp = Path(tempfile.mkdtemp(prefix="lesson_templates_"))
    return extract_templates(reference_dir, tmp)
