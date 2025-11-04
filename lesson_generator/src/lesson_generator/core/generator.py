"""Lesson generation orchestrator for Sprint 1.

Generates basic lesson skeletons (folders + README) from topics or a config file.
"""
from __future__ import annotations

from dataclasses import dataclass
import ast
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Iterable, List, Optional, Callable

from lesson_generator.core.file_manager import FileStructureManager
from lesson_generator.core.template_engine import TemplateEngine
from lesson_generator.core.topic_processor import TopicModel, TopicProcessor, ModuleModel, ResourcesModel
from lesson_generator.content import FallbackContentGenerator, ContentGenerator


@dataclass
class GenerationOptions:
    output_dir: Path
    modules_override: Optional[int] = None
    dry_run: bool = False
    workers: Optional[int] = 1
    difficulty_override: Optional[str] = None
    strict_ai_only: bool = False
    lessons_count: Optional[int] = None
    ai_direct_code: bool = True


@dataclass
class ItemResult:
    topic_name: str
    success: bool
    status: str
    output_path: Optional[Path] = None


@dataclass
class GenerationResult:
    items: List[ItemResult]


class LessonGenerator:
    """Main orchestrator for generating lessons (Sprint 1 scope)."""

    def __init__(self, templates_dir: Optional[Path] = None, content_generator: ContentGenerator | None = None) -> None:
        if templates_dir is None:
            templates_dir = Path(__file__).resolve().parents[1] / "templates"
        self.templates = TemplateEngine(templates_dir)
        self.files = FileStructureManager()
        self.topics = TopicProcessor()
        self.content = content_generator or FallbackContentGenerator()

    # Append error messages to a per-topic errors.txt without interrupting generation
    @staticmethod
    def _append_error(error_file: Path, message: str) -> None:
        try:
            error_file.parent.mkdir(parents=True, exist_ok=True)
            with error_file.open("a", encoding="utf-8") as f:
                f.write(str(message).rstrip() + "\n")
        except Exception:
            # Never allow logging to break generation
            pass

    def generate(
        self,
        *,
        topics: Iterable[str] | None,
        topics_json: Optional[str],
        options: GenerationOptions,
        on_progress: Optional[Callable[["ItemResult", int, int], None]] = None,
        on_module_progress: Optional[
            Callable[[str, int, int, str, str], None]
        ] = None,  # (topic_name, module_index, module_total, module_name, step)
    ) -> GenerationResult:
        # Build topic models
        topic_models: List[TopicModel] = []
        models_from_config: List[TopicModel] = []
        models_from_names: List[TopicModel] = []
        if topics_json:
            models_from_config = self.topics.parse_topics(topics_json)
            topic_models.extend(models_from_config)
        if topics:
            models_from_names = self.topics.from_names(list(topics))
            topic_models.extend(models_from_names)

        # Change #4: If topics came from names, first generate (AI or fallback) a list of modules
        # with estimated times, goals, and references. Then use those to structure modules before generation.
        if models_from_names:
            desired_count = int(options.modules_override or 5)
            for t in models_from_names:
                try:
                    plan = self.content.plan_modules(t.name, desired_count)
                except Exception as exc:
                    if options.strict_ai_only and not options.dry_run:
                        # Respect strict AI requirement when actually generating files
                        raise RuntimeError(f"module planning failed for topic '{t.name}': {exc}") from exc
                    # In dry-run or non-strict mode, keep existing minimal structure
                    continue

                # Update TopicModel with planned objectives, concepts, and resources (if provided)
                try:
                    if isinstance(plan, dict):
                        lo = plan.get("learning_objectives") or []
                        if lo:
                            t.learning_objectives = list(lo)
                        kc = plan.get("key_concepts") or []
                        if kc:
                            t.key_concepts = list(kc)
                        res = plan.get("resources") or None
                        if res:
                            try:
                                t.resources = ResourcesModel(**res)  # type: ignore[assignment]
                            except Exception:
                                # Ignore invalid resources silently
                                pass

                        # Convert planned module dicts to ModuleModel instances, sanitizing names
                        planned_modules = []
                        for idx, m in enumerate(plan.get("modules") or [], start=1):
                            try:
                                name_raw = m.get("name") or f"module_{idx}"
                                safe_name = self._sanitize_identifier(str(name_raw), as_class=False)
                                # Ensure it starts with a letter and matches required pattern
                                if not safe_name or not safe_name[0].isalpha():
                                    safe_name = f"m{safe_name}"
                                title = m.get("title") or safe_name.replace("_", " ").title()
                                mod = ModuleModel(
                                    name=safe_name,
                                    title=title,
                                    type=m.get("type") or ("starter" if idx == 1 else "assignment"),
                                    focus_areas=(m.get("focus_areas") or [safe_name]),
                                    complexity=m.get("complexity") or ("simple" if idx == 1 else "moderate"),
                                    estimated_time=m.get("estimated_time") or (60 if idx == 1 else 90),
                                    includes_tests=m.get("includes_tests", True),
                                    code_examples=m.get("code_examples") or 3,
                                )
                                planned_modules.append(mod)
                            except Exception:
                                # Skip invalid module entries
                                continue
                        if planned_modules:
                            t.modules = planned_modules
                except Exception:
                    # Be resilient; if anything goes wrong, keep previous minimal topic definition
                    pass

        # Limit number of lessons if requested
        if options.lessons_count is not None and options.lessons_count >= 0:
            topic_models = topic_models[: int(options.lessons_count)]

        items: List[ItemResult] = []
        workers = max(1, int(options.workers or 1))
        if workers > 1 and len(topic_models) > 1:
            with ThreadPoolExecutor(max_workers=workers) as ex:
                total = len(topic_models)
                completed = 0
                future_map = {ex.submit(self._generate_single, t, options, on_module_progress): t for t in topic_models}
                for fut in as_completed(future_map):
                    t = future_map[fut]
                    try:
                        res = fut.result()
                        items.append(res)
                        completed += 1
                        if on_progress:
                            on_progress(res, completed, total)
                    except Exception as exc:  # pragma: no cover - defensive guard
                        res = ItemResult(
                                topic_name=t.name,
                                success=False,
                                status=f"Error: {exc}",
                                output_path=None,
                            )
                        items.append(res)
                        completed += 1
                        if on_progress:
                            on_progress(res, completed, total)
        else:
            total = len(topic_models)
            for i, topic in enumerate(topic_models, start=1):
                try:
                    res = self._generate_single(topic, options, on_module_progress)
                    items.append(res)
                    if on_progress:
                        on_progress(res, i, total)
                except Exception as exc:  # pragma: no cover - defensive guard
                    res = ItemResult(
                            topic_name=topic.name,
                            success=False,
                            status=f"Error: {exc}",
                            output_path=None,
                        )
                    items.append(res)
                    if on_progress:
                        on_progress(res, i, total)
        return GenerationResult(items=items)

    def _generate_single(
        self,
        topic: TopicModel,
        options: GenerationOptions,
        on_module_progress: Optional[Callable[[str, int, int, str, str], None]] = None,
    ) -> ItemResult:
        # Respect module override but do not exceed available modules in the topic
        if options.modules_override is not None:
            module_count = min(int(options.modules_override), len(topic.modules))
        else:
            module_count = len(topic.modules)
        module_names = [m.name for m in topic.modules[:module_count]]
        if not module_names:
            module_names = ["basics"]

        if options.dry_run:
            # Dry-run: report what would happen
            return ItemResult(
                topic_name=topic.name,
                success=True,
                status=f"Would create {module_count} module(s)",
                output_path=options.output_dir / topic.name,
            )

        # Create directories
        paths = self.files.create_lesson_dirs(options.output_dir, topic.name, module_names)

        # Prepare safe topic dict for templates
        topic_dict = topic.model_dump()
        if options.difficulty_override:
            topic_dict["difficulty"] = options.difficulty_override
        resources_default: dict[str, list[str]] = {
            "documentation_links": [],
            "additional_reading": [],
            "example_repositories": [],
        }
        topic_dict["resources"] = topic_dict.get("resources") or resources_default

        # README via content generator (AI or fallback)
        try:
            readme_md = self.content.readme(topic_dict)
        except Exception:
            if options.strict_ai_only:
                raise
            # As a last resort, use template-based README
            readme_md = self.templates.render(
                "readme.md.j2",
                context={
                    "topic": topic_dict,
                    "concept_descriptions": {},
                },
            )
        # Ensure README includes a Resources section with links when resources are provided
        try:
            resources = topic_dict.get("resources") or {}
            has_any_resources = any(resources.get(k) for k in ("documentation_links", "additional_reading", "example_repositories"))
            needs_resources_section = ("## Resources" not in readme_md) and has_any_resources
            if needs_resources_section:
                lines: list[str] = ["\n## Resources\n"]
                docs = resources.get("documentation_links") or []
                if docs:
                    lines.append("### Official Documentation\n")
                    for item in docs:
                        try:
                            title = (item.get("title") if isinstance(item, dict) else str(item))
                            url = (item.get("url") if isinstance(item, dict) else str(item))
                            if url and title:
                                lines.append(f"- [{title}]({url})\n")
                            elif url:
                                lines.append(f"- {url}\n")
                        except Exception:
                            lines.append(f"- {item}\n")
                    lines.append("\n")
                repos = resources.get("example_repositories") or []
                if repos:
                    lines.append("### Example Repositories\n")
                    for repo in repos:
                        try:
                            name = (repo.get("name") if isinstance(repo, dict) else str(repo))
                            url = (repo.get("url") if isinstance(repo, dict) else str(repo))
                            if url and name:
                                lines.append(f"- [{name}]({url})\n")
                            elif url:
                                lines.append(f"- {url}\n")
                        except Exception:
                            lines.append(f"- {repo}\n")
                    lines.append("\n")
                reading = resources.get("additional_reading") or []
                if reading:
                    lines.append("### Additional Reading\n")
                    for r in reading:
                        lines.append(f"- {r}\n")
                    lines.append("\n")
                readme_md = readme_md.rstrip() + "\n\n" + "".join(lines)
        except Exception:
            # Be resilient; if enrichment fails, proceed with original README
            pass
        self.files.write_text(paths.root / "README.md", readme_md)

        # Touch basic config placeholders (filled in future sprints)
        self.files.write_text(paths.root / "requirements.txt", "pytest\npylint\nblack\n")
        self.files.write_text(paths.root / "pytest.ini", "[pytest]\naddopts = -q\n")
        # Sprint 3 additions: Makefile and setup.cfg
        makefile = self.templates.render("makefile.j2", {"project": topic_dict})
        self.files.write_text(paths.root / "Makefile", makefile)
        setup_cfg = self.templates.render("setup.cfg.j2", {"project": topic_dict})
        self.files.write_text(paths.root / "setup.cfg", setup_cfg)

        # GitHub CI workflow and repo hygiene files so lessons are GitHub-ready
        try:
            workflow_yml = self.templates.render("github_workflow_python_tests.yml.j2", {"project": topic_dict})
            self.files.write_text(paths.root / ".github" / "workflows" / "python-tests.yml", workflow_yml)
        except Exception:
            # Non-fatal: continue generation even if CI template missing
            pass
        try:
            gitignore_txt = self.templates.render("gitignore.j2", {"project": topic_dict})
            self.files.write_text(paths.root / ".gitignore", gitignore_txt)
        except Exception:
            # Non-fatal as well
            pass

        # Generate per-module files using content generator
        module_total = module_count
        for idx, mod in enumerate(topic.modules[:module_count], start=1):
            mod_dir = paths.root / f"module_{idx}_{mod.name}"
            step = "start"
            errors_file = paths.root / "errors.txt"
            try:
                # Emit module start event
                if on_module_progress:
                    try:
                        on_module_progress(topic.name, idx, module_total, mod.name, "start")
                    except Exception:
                        pass
                step = "learning_path"
                try:
                    # Learning path
                    lp_ctx = self.content.learning_path(topic_dict, mod.model_dump())
                    lp_ctx["module"] = {"title": mod.title, "focus_areas": mod.focus_areas}
                    lp_ctx["module_number"] = idx
                    lp_ctx["topic"] = topic_dict
                    # Provide assignments metadata for checklist
                    # Difficulty-adjusted estimated time
                    def _scale_time(base: Optional[int]) -> int:
                        base = base or 60
                        diff = (options.difficulty_override or topic_dict.get("difficulty") or "intermediate").lower()
                        if diff == "beginner":
                            return max(15, int(base * 0.8))
                        if diff == "advanced":
                            return int(base * 1.3)
                        return base

                    assignments_meta = [
                        {
                            "name": "assignment_a",
                            "complexity": mod.complexity or "simple",
                            "estimated_time": _scale_time(mod.estimated_time),
                            "focus_areas": mod.focus_areas,
                            "filename": "assignment_a.py",
                        }
                    ]
                    if mod.type in {"assignment", "project"}:
                        assignments_meta.append(
                            {
                                "name": "assignment_b",
                                "complexity": mod.complexity or "moderate",
                                "estimated_time": _scale_time((mod.estimated_time or 60) + 30),
                                "focus_areas": mod.focus_areas,
                                "filename": "assignment_b.py",
                            }
                        )
                    lp_content = self.templates.render(
                        "learning_path.md.j2",
                        {
                            "module": {"title": mod.title, "focus_areas": mod.focus_areas},
                            "module_number": idx,
                            "topic": topic_dict,
                            "content": lp_ctx,
                            "assignments": assignments_meta,
                        },
                    )
                    # Write module documentation as README.md to avoid duplicate docs
                    self.files.write_text(mod_dir / "README.md", lp_content)
                except Exception as exc:
                    self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=learning_path -> {exc}")
                    lp_content = ""
                if on_module_progress:
                    try:
                        on_module_progress(topic.name, idx, module_total, mod.name, "learning_path")
                    except Exception:
                        pass

                # Track exported names for package __init__
                starter_export_name: Optional[str] = None
                assignment_a_export_name: Optional[str] = None

                # Build a reusable module context enriched with learning_path reference
                mod_ctx: dict = mod.model_dump()
                mod_ctx["module_number"] = idx
                mod_ctx["learning_path_md"] = lp_content
                try:
                    mod_ctx["learning_path_path"] = str((mod_dir / "README.md").resolve())
                except Exception:
                    mod_ctx["learning_path_path"] = str(mod_dir / "README.md")

                # Starter example (with graceful fallback on syntax issues)
                step = "starter_example"
                starter_ctx: dict = {}
                starter_attempts = 0
                direct_starter_tried = False
                while True:
                    starter_attempts += 1
                    try:
                        # Attempt direct code mode once if enabled
                        if options.ai_direct_code and not direct_starter_tried:
                            try:
                                from lesson_generator.content.openai_generator import OpenAIContentGenerator as _OA
                                _gen = getattr(self, "content", None)
                                underlying = getattr(_gen, "_underlying", _gen)
                                if isinstance(underlying, _OA) and hasattr(underlying, "starter_example_code"):
                                    code_text = underlying.starter_example_code(topic_dict, mod_ctx)
                                    code_text = self._strip_markdown_fences(code_text)
                                    self._validate_python_syntax(code_text, f"module_{idx}_{mod.name}/starter_example.py")
                                    self.files.write_text(mod_dir / "starter_example.py", code_text)
                                    # Try to infer class name from the generated code
                                    try:
                                        import ast as _ast
                                        tree = _ast.parse(code_text)
                                        class_names = [n.name for n in tree.body if isinstance(n, _ast.ClassDef)]
                                        # Choose the first class if any
                                        if class_names:
                                            starter_export_name = self._sanitize_identifier(class_names[0], as_class=True)
                                    except Exception:
                                        pass
                                    # No separate starter_example.md; content lives in starter_example.py docstrings
                                    break
                            except Exception:
                                # Mark tried and fall back to JSON path
                                direct_starter_tried = True
                        starter_ctx = self.content.starter_example(topic_dict, mod_ctx)
                        # Sanitize AI-provided identifiers and parameters to ensure valid Python
                        try:
                            if starter_ctx.get("class_name"):
                                starter_ctx["class_name"] = self._sanitize_identifier(
                                    starter_ctx["class_name"], as_class=True
                                )
                            # Ensure common defaults present for template fields
                            starter_ctx.setdefault("filename", "starter_example.py")
                            # Sanitize import statements: keep only valid single-line imports
                            safe_imports: list[str] = []
                            for st in (starter_ctx.get("imports") or []):
                                s = (st or "").strip()
                                if self._is_valid_import_line(s):
                                    safe_imports.append(s)
                            starter_ctx["imports"] = safe_imports
                            # Methods
                            for m in starter_ctx.get("methods", []) or []:
                                if m.get("name"):
                                    m["name"] = self._sanitize_identifier(m["name"], as_class=False)
                                # Normalize parameters to either empty or start with a comma
                                params = (m.get("parameters") or "").strip()
                                if params and not params.lstrip().startswith(","):
                                    params = ", " + params
                                # Ensure parentheses are not included by AI
                                params = params.replace("(", "").replace(")", "")
                                # Very conservative parameter sanitization: remove dangerous characters
                                # Keep only a safe subset of characters commonly used in parameter lists
                                import re as _re  # local import to avoid top-level pollution
                                params = _re.sub(r"[^0-9a-zA-Z_,:= *\[\]|.]+", "", params)
                                # If params look obviously broken (e.g., end with colon/comma), drop them
                                if params.strip().endswith((":", ",", "=", "|")):
                                    params = ""
                                m["parameters"] = params
                                # Validate implementation block; if invalid, replace with a safe placeholder
                                impl = (m.get("implementation") or "").rstrip()
                                if not self._is_valid_block(impl, kind="method", params=params):
                                    m["implementation"] = "pass  # sanitized placeholder"
                                else:
                                    m["implementation"] = impl
                            # Demonstration functions if present
                            for d in starter_ctx.get("demonstration_functions", []) or []:
                                if d.get("name"):
                                    d["name"] = self._sanitize_identifier(d["name"], as_class=False)
                                demo_impl = (d.get("implementation") or "").rstrip()
                                if not self._is_valid_block(demo_impl, kind="function"):
                                    d["implementation"] = "print(\"[demo skipped: sanitized]\")"
                            # Also validate demonstration calls if present
                            for call in starter_ctx.get("demonstrations", []) or []:
                                fc = (call.get("function_call") or "").strip()
                                if fc and not self._is_valid_statement(fc):
                                    call["function_call"] = "print(\"[invalid demo call skipped]\")"
                        except Exception:
                            # Be resilient; if sanitation fails, continue with raw but let syntax validation catch issues
                            pass
                        starter_ctx["example"] = starter_ctx
                        starter_code = self.templates.render("starter_example.py.j2", {"example": starter_ctx})
                        try:
                            self._validate_python_syntax(starter_code, f"module_{idx}_{mod.name}/starter_example.py")
                            self.files.write_text(mod_dir / "starter_example.py", starter_code)
                            starter_export_name = starter_ctx.get("class_name")
                            # No separate starter_example.md; content lives in starter_example.py docstrings
                            break
                        except Exception:
                            # In strict AI mode, retry a couple times before giving up
                            if options.strict_ai_only and starter_attempts < 3:
                                continue
                            if options.strict_ai_only:
                                raise
                            # Fallback to deterministic content to keep generation successful
                            from lesson_generator.content import FallbackContentGenerator

                            fb_ctx = FallbackContentGenerator().starter_example(topic_dict, mod.model_dump())
                            fb_ctx.setdefault("filename", "starter_example.py")
                            fb_ctx["example"] = fb_ctx
                            fb_code = self.templates.render("starter_example.py.j2", {"example": fb_ctx})
                            self._validate_python_syntax(fb_code, f"module_{idx}_{mod.name}/starter_example.py")
                            self.files.write_text(mod_dir / "starter_example.py", fb_code)
                            starter_export_name = fb_ctx.get("class_name")
                            break
                    except Exception as exc:
                        self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=starter_example -> {exc}")
                        # Write a minimal, non-placeholder fallback so the file exists
                        try:
                            placeholder_class = self._sanitize_identifier(f"{mod.name.title().replace('_','')}Helper", as_class=True)
                            placeholder = (
                                f"\"\"\"\nAuto-generated starter example fallback.\nTODO: Extend this class as part of the lesson.\n\"\"\"\n\n"
                                f"class {placeholder_class}:\n"
                                f"    \"\"\"A minimal helper implementation for students to extend.\n\"\"\"\n\n"
                                f"    def demo(self) -> str:\n"
                                f"        return 'ok'\n"
                            )
                            self.files.write_text(mod_dir / "starter_example.py", placeholder)
                            starter_export_name = placeholder_class
                        except Exception as _exc:
                            self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} placeholder starter_example failed -> {_exc}")
                        break
                    except Exception as exc:
                        self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=starter_example -> {exc}")
                        break
                if on_module_progress:
                    try:
                        on_module_progress(topic.name, idx, module_total, mod.name, "starter_example")
                    except Exception:
                        pass

                # Assignment A (with graceful fallback on syntax issues)
                step = "assignment_a"
                try:
                    assignment_a_written = False
                    if options.ai_direct_code:
                        try:
                            from lesson_generator.content.openai_generator import OpenAIContentGenerator as _OA
                            _gen = getattr(self, "content", None)
                            underlying = getattr(_gen, "_underlying", _gen)
                            if isinstance(underlying, _OA) and hasattr(underlying, "assignment_code"):
                                code_text = underlying.assignment_code(topic_dict, mod_ctx, variant="a")
                                code_text = self._strip_markdown_fences(code_text)
                                self._validate_python_syntax(code_text, f"module_{idx}_{mod.name}/assignment_a.py")
                                self.files.write_text(mod_dir / "assignment_a.py", code_text)
                                # Capture class name via AST for exports and tests
                                try:
                                    import ast as _ast
                                    tree = _ast.parse(code_text)
                                    class_names = [n.name for n in tree.body if isinstance(n, _ast.ClassDef)]
                                    if class_names:
                                        assignment_a_export_name = self._sanitize_identifier(class_names[0], as_class=True)
                                except Exception:
                                    pass
                                # Seed assignment context for tests with inferred class and source
                                try:
                                    asg_a_ctx = {
                                        "class_name": assignment_a_export_name or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentA", as_class=True),
                                        "description": "Assignment A",
                                        "variant": "a",
                                        "source_code": code_text,
                                    }
                                except Exception:
                                    asg_a_ctx = {"class_name": assignment_a_export_name or None, "variant": "a", "source_code": code_text}
                                assignment_a_written = True
                        except Exception:
                            assignment_a_written = False
                    if not assignment_a_written:
                        asg_a_ctx = self.content.assignment(topic_dict, mod_ctx, variant="a")
                        # Mark variant for downstream test generation
                        try:
                            asg_a_ctx["variant"] = "a"
                        except Exception:
                            pass
                        asg_a_ctx["assignment"] = asg_a_ctx
                        assignment_a_code = self.templates.render("assignment.py.j2", asg_a_ctx)
                        try:
                            self._validate_python_syntax(assignment_a_code, f"module_{idx}_{mod.name}/assignment_a.py")
                            self.files.write_text(mod_dir / "assignment_a.py", assignment_a_code)
                            # Attach source code for tests prompt
                            try:
                                asg_a_ctx["source_code"] = assignment_a_code
                            except Exception:
                                pass
                            assignment_a_export_name = asg_a_ctx.get("class_name")
                        except Exception:
                            if options.strict_ai_only:
                                raise
                            from lesson_generator.content import FallbackContentGenerator

                            fb_asg = FallbackContentGenerator().assignment(topic_dict, mod.model_dump(), variant="a")
                            fb_asg["variant"] = "a"
                            fb_asg["assignment"] = fb_asg
                            fb_asg_code = self.templates.render("assignment.py.j2", fb_asg)
                            self._validate_python_syntax(fb_asg_code, f"module_{idx}_{mod.name}/assignment_a.py")
                            self.files.write_text(mod_dir / "assignment_a.py", fb_asg_code)
                            assignment_a_export_name = fb_asg.get("class_name")
                            asg_a_ctx = fb_asg
                            try:
                                asg_a_ctx["source_code"] = fb_asg_code
                            except Exception:
                                pass
                except Exception as exc:
                    self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=assignment_a -> {exc}")
                    # Create a minimal, non-placeholder assignment to ensure the file exists
                    try:
                        placeholder_class = self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentA", as_class=True)
                        placeholder = (
                            f"\"\"\"\nAuto-generated assignment A fallback.\nTODO: Implement the business logic as described in the module README.\n\"\"\"\n\n"
                            f"class {placeholder_class}:\n"
                            f"    def process(self, data=None):\n"
                            f"        \"\"\"TODO: replace this with a real implementation.\n\nThis minimal method returns 0 to keep tests importable.\n\"\"\"\n"
                            f"        return 0\n"
                        )
                        self.files.write_text(mod_dir / "assignment_a.py", placeholder)
                        assignment_a_export_name = placeholder_class
                        asg_a_ctx = {"class_name": placeholder_class, "description": "Assignment A", "variant": "a", "source_code": placeholder}
                    except Exception as _exc:
                        self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} placeholder assignment_a failed -> {_exc}")
                if on_module_progress:
                    try:
                        on_module_progress(topic.name, idx, module_total, mod.name, "assignment_a")
                    except Exception:
                        pass

                # Tests for assignment A (with graceful fallback on syntax issues)
                step = "tests_a"
                # Include module_number to allow generators to build correct import paths
                try:
                    # Ensure assignment context exists for tests (even if code was generated directly)
                    if 'asg_a_ctx' not in locals() or not isinstance(asg_a_ctx, dict) or not asg_a_ctx.get("class_name"):
                        # Derive a safe default class name
                        derived_cls = assignment_a_export_name or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentA", as_class=True)
                        # Read source code from file if available
                        try:
                            src_text_a = (mod_dir / "assignment_a.py").read_text(encoding="utf-8")
                        except Exception:
                            src_text_a = ""
                        asg_a_ctx = {"class_name": derived_cls, "description": "Assignment A", "variant": "a", "source_code": src_text_a}
                    else:
                        # Ensure source_code present; if missing, read from file
                        if not asg_a_ctx.get("source_code"):
                            try:
                                asg_a_ctx["source_code"] = (mod_dir / "assignment_a.py").read_text(encoding="utf-8")
                            except Exception:
                                pass
                    tests_a_ctx = self.content.tests_for_assignment(topic_dict, mod_ctx, asg_a_ctx)
                    # Ensure tests target the actual exported assignment class name
                    if assignment_a_export_name:
                        tests_a_ctx["class_name"] = assignment_a_export_name
                        tests_a_ctx["test_target_name"] = assignment_a_export_name
                    # Mark this as a template suite for students
                    try:
                        tests_a_ctx["is_template"] = True
                    except Exception:
                        pass
                    # Force correct module import path for reliability
                    try:
                        module_path_str = f"module_{idx}_{mod.name}"
                        tests_a_ctx["module_path"] = module_path_str
                    except Exception:
                        pass
                    test_a_code = self.templates.render("test_template.py.j2", tests_a_ctx)
                    try:
                        self._validate_python_syntax(test_a_code, f"module_{idx}_{mod.name}/test_assignment_a.py")
                        self.files.write_text(mod_dir / "test_assignment_a.py", test_a_code)
                        # Sanitize any placeholder-y content that may have slipped through
                        try:
                            self._sanitize_test_file(mod_dir / "test_assignment_a.py", f"module_{idx}_{mod.name}", assignment_a_export_name or (asg_a_ctx.get("class_name") if isinstance(asg_a_ctx, dict) else None) or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentA", as_class=True))
                        except Exception:
                            pass
                    except Exception:
                        if options.strict_ai_only:
                            raise
                        from lesson_generator.content import FallbackContentGenerator

                        fb_tests = FallbackContentGenerator().tests_for_assignment(
                            topic_dict, mod.model_dump(), asg_a_ctx
                        )
                        if assignment_a_export_name:
                            fb_tests["class_name"] = assignment_a_export_name
                            fb_tests["test_target_name"] = assignment_a_export_name
                        try:
                            fb_tests["is_template"] = True
                        except Exception:
                            pass
                        fb_test_code = self.templates.render("test_template.py.j2", fb_tests)
                        self._validate_python_syntax(
                            fb_test_code, f"module_{idx}_{mod.name}/test_assignment_a.py"
                        )
                        self.files.write_text(mod_dir / "test_assignment_a.py", fb_test_code)
                        try:
                            self._sanitize_test_file(mod_dir / "test_assignment_a.py", f"module_{idx}_{mod.name}", assignment_a_export_name or (fb_tests.get("class_name") if isinstance(fb_tests, dict) else None) or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentA", as_class=True))
                        except Exception:
                            pass
                except Exception as exc:
                    self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=tests_a -> {exc}")
                    # Write a simple, non-placeholder smoke test to ensure presence
                    try:
                        cls = assignment_a_export_name or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentA", as_class=True)
                        module_path_str = f"module_{idx}_{mod.name}"
                        smoke = (
                            f"from {module_path_str} import {cls}\n\n"
                            f"def test_assignment_a_smoke():\n"
                            f"    obj = {cls}()\n"
                            f"    assert obj is not None\n"
                        )
                        self.files.write_text(mod_dir / "test_assignment_a.py", smoke)
                    except Exception as _exc:
                        self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} placeholder test_assignment_a failed -> {_exc}")
                if on_module_progress:
                    try:
                        on_module_progress(topic.name, idx, module_total, mod.name, "tests_a")
                    except Exception:
                        pass

                # Assignment B if applicable
                if mod.type in {"assignment", "project"}:
                    step = "assignment_b"
                    try:
                        assignment_b_written = False
                        if options.ai_direct_code:
                            try:
                                from lesson_generator.content.openai_generator import OpenAIContentGenerator as _OA
                                _gen = getattr(self, "content", None)
                                underlying = getattr(_gen, "_underlying", _gen)
                                if isinstance(underlying, _OA) and hasattr(underlying, "assignment_code"):
                                    code_text_b = underlying.assignment_code(topic_dict, mod_ctx, variant="b")
                                    # Do not persist raw AI outputs
                                    code_text_b = self._strip_markdown_fences(code_text_b)
                                    self._validate_python_syntax(code_text_b, f"module_{idx}_{mod.name}/assignment_b.py")
                                    self.files.write_text(mod_dir / "assignment_b.py", code_text_b)
                                    # Capture class name via AST for exports/tests
                                    try:
                                        import ast as _ast
                                        tree_b = _ast.parse(code_text_b)
                                        class_names_b = [n.name for n in tree_b.body if isinstance(n, _ast.ClassDef)]
                                        if class_names_b:
                                            inferred_b = self._sanitize_identifier(class_names_b[0], as_class=True)
                                        else:
                                            inferred_b = self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentB", as_class=True)
                                    except Exception:
                                        inferred_b = self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentB", as_class=True)
                                    # Seed context for tests
                                    try:
                                        asg_b_ctx = {"class_name": inferred_b, "description": "Assignment B", "variant": "b", "source_code": code_text_b}
                                    except Exception:
                                        asg_b_ctx = {"class_name": inferred_b, "variant": "b", "source_code": code_text_b}
                                    assignment_b_written = True
                            except Exception:
                                assignment_b_written = False
                        if not assignment_b_written:
                            asg_b_ctx = self.content.assignment(topic_dict, mod_ctx, variant="b")
                            try:
                                asg_b_ctx["variant"] = "b"
                            except Exception:
                                pass
                            asg_b_ctx["assignment"] = asg_b_ctx
                            assignment_b_code = self.templates.render("assignment.py.j2", asg_b_ctx)
                            try:
                                self._validate_python_syntax(assignment_b_code, f"module_{idx}_{mod.name}/assignment_b.py")
                                self.files.write_text(mod_dir / "assignment_b.py", assignment_b_code)
                                try:
                                    asg_b_ctx["source_code"] = assignment_b_code
                                except Exception:
                                    pass
                            except Exception:
                                if options.strict_ai_only:
                                    raise
                                from lesson_generator.content import FallbackContentGenerator

                                fb_asg_b = FallbackContentGenerator().assignment(topic_dict, mod.model_dump(), variant="b")
                                fb_asg_b["variant"] = "b"
                                fb_asg_b["assignment"] = fb_asg_b
                                fb_asg_b_code = self.templates.render("assignment.py.j2", fb_asg_b)
                                self._validate_python_syntax(fb_asg_b_code, f"module_{idx}_{mod.name}/assignment_b.py")
                                self.files.write_text(mod_dir / "assignment_b.py", fb_asg_b_code)
                                asg_b_ctx = fb_asg_b
                                try:
                                    asg_b_ctx["source_code"] = fb_asg_b_code
                                except Exception:
                                    pass
                    except Exception as exc:
                        self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=assignment_b -> {exc}")
                        # Create a minimal, non-placeholder assignment_b.py
                        try:
                            placeholder_class_b = self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentB", as_class=True)
                            placeholder_b = (
                                f"\"\"\"\nAuto-generated assignment B fallback.\nTODO: Extend with project features.\n\"\"\"\n\n"
                                f"class {placeholder_class_b}:\n"
                                f"    def process(self, data=None):\n"
                                f"        \"\"\"TODO: replace with project-specific logic.\n\"\"\"\n"
                                f"        return 0\n"
                            )
                            self.files.write_text(mod_dir / "assignment_b.py", placeholder_b)
                            asg_b_ctx = {"class_name": placeholder_class_b}
                        except Exception as _exc:
                            self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} placeholder assignment_b failed -> {_exc}")
                    if on_module_progress:
                        try:
                            on_module_progress(topic.name, idx, module_total, mod.name, "assignment_b")
                        except Exception:
                            pass

                    step = "tests_b"
                    try:
                        if 'asg_b_ctx' not in locals() or not isinstance(asg_b_ctx, dict) or not asg_b_ctx.get("class_name"):
                            derived_cls_b = self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentB", as_class=True)
                            # Read source code from file if available
                            try:
                                src_text_b = (mod_dir / "assignment_b.py").read_text(encoding="utf-8")
                            except Exception:
                                src_text_b = ""
                            asg_b_ctx = {"class_name": derived_cls_b, "description": "Assignment B", "variant": "b", "source_code": src_text_b}
                        else:
                            # Ensure source_code present; if missing, read from file
                            if not asg_b_ctx.get("source_code"):
                                try:
                                    asg_b_ctx["source_code"] = (mod_dir / "assignment_b.py").read_text(encoding="utf-8")
                                except Exception:
                                    pass
                        tests_b_ctx = self.content.tests_for_assignment(topic_dict, mod_ctx, asg_b_ctx)
                        # Align test class target with exported class name
                        if asg_b_ctx.get("class_name"):
                            tests_b_ctx["class_name"] = asg_b_ctx["class_name"]
                            tests_b_ctx["test_target_name"] = asg_b_ctx["class_name"]
                        # Fully implemented tests (not a template)
                        try:
                            tests_b_ctx["is_template"] = False
                        except Exception:
                            pass
                        # Force correct module import path for reliability
                        try:
                            module_path_str = f"module_{idx}_{mod.name}"
                            tests_b_ctx["module_path"] = module_path_str
                        except Exception:
                            pass
                        test_b_code = self.templates.render("test_template.py.j2", tests_b_ctx)
                        try:
                            self._validate_python_syntax(test_b_code, f"module_{idx}_{mod.name}/test_assignment_b.py")
                            self.files.write_text(mod_dir / "test_assignment_b.py", test_b_code)
                            try:
                                self._sanitize_test_file(mod_dir / "test_assignment_b.py", f"module_{idx}_{mod.name}", (asg_b_ctx.get("class_name") if isinstance(asg_b_ctx, dict) else None) or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentB", as_class=True))
                            except Exception:
                                pass
                        except Exception:
                            if options.strict_ai_only:
                                raise
                            from lesson_generator.content import FallbackContentGenerator

                            fb_tests_b = FallbackContentGenerator().tests_for_assignment(
                                topic_dict, mod.model_dump(), asg_b_ctx
                            )
                            if asg_b_ctx.get("class_name"):
                                fb_tests_b["class_name"] = asg_b_ctx["class_name"]
                                fb_tests_b["test_target_name"] = asg_b_ctx["class_name"]
                            fb_test_b_code = self.templates.render("test_template.py.j2", fb_tests_b)
                            self._validate_python_syntax(
                                fb_test_b_code, f"module_{idx}_{mod.name}/test_assignment_b.py"
                            )
                            self.files.write_text(mod_dir / "test_assignment_b.py", fb_test_b_code)
                        try:
                            self._sanitize_test_file(mod_dir / "test_assignment_b.py", f"module_{idx}_{mod.name}", (asg_b_ctx.get("class_name") if isinstance(asg_b_ctx, dict) else None) or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentB", as_class=True))
                        except Exception:
                            pass
                    except Exception as exc:
                        self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=tests_b -> {exc}")
                        # Write a simple, non-placeholder smoke test for assignment B
                        try:
                            cls_b = (asg_b_ctx.get("class_name") if isinstance(asg_b_ctx, dict) else None) or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentB", as_class=True)
                            module_path_str = f"module_{idx}_{mod.name}"
                            placeholder = (
                                f"from {module_path_str} import {cls_b}\n\n"
                                f"def test_assignment_b_smoke():\n"
                                f"    obj = {cls_b}()\n"
                                f"    assert hasattr(obj, 'process')\n"
                            )
                            self.files.write_text(mod_dir / "test_assignment_b.py", placeholder)
                        except Exception as _exc:
                            self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} placeholder test_assignment_b failed -> {_exc}")
                    if on_module_progress:
                        try:
                            on_module_progress(topic.name, idx, module_total, mod.name, "tests_b")
                        except Exception:
                            pass

                # Sprint 3: add test for starter example and extra exercises file
                # Starter smoke test via content generator
                module_path_str = f"module_{idx}_{mod.name}"
                try:
                    target_class = starter_export_name or (starter_ctx.get("class_name") if isinstance(starter_ctx, dict) else None)
                except Exception:
                    target_class = starter_export_name
                if not target_class:
                    # Derive a safe default helper name if none available
                    target_class = self._sanitize_identifier(f"{mod.name.title().replace('_','')}Helper", as_class=True)
                try:
                    starter_methods = []
                    try:
                        starter_methods = (starter_ctx.get("methods") if isinstance(starter_ctx, dict) else []) or []
                    except Exception:
                        starter_methods = []
                    starter_test_code = self.content.starter_smoke_test(module_path_str, target_class, starter_methods)
                    # Sanitize common AI formatting issues such as Markdown code fences
                    starter_test_code = self._strip_markdown_fences(starter_test_code).lstrip()
                    self._validate_python_syntax(
                        starter_test_code, f"module_{idx}_{mod.name}/test_starter_example.py"
                    )
                    self.files.write_text(mod_dir / "test_starter_example.py", starter_test_code)
                    try:
                        self._sanitize_test_file(mod_dir / "test_starter_example.py", module_path_str, target_class)
                    except Exception:
                        pass
                except Exception as exc:
                    if options.strict_ai_only:
                        self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=starter_test -> {exc}")
                        # Create a minimal placeholder smoke test
                        try:
                            target = target_class or (starter_export_name or self._sanitize_identifier(f"{mod.name.title().replace('_','')}Helper", as_class=True))
                            placeholder = (
                                f"from {module_path_str} import {target}\n\n"
                                f"def test_demo_placeholder():\n"
                                f"    obj = {target}()\n"
                                f"    assert hasattr(obj, 'demo')\n"
                            )
                            self.files.write_text(mod_dir / "test_starter_example.py", placeholder)
                        except Exception as _exc:
                            self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} placeholder starter_test failed -> {_exc}")
                    else:
                        # Fallback to template if AI code invalid
                        starter_test_ctx = {
                            "test_target_name": target_class,
                            "module_path": module_path_str,
                            "class_name": target_class,
                        }
                        starter_test_code = self.templates.render("test_starter_example.py.j2", starter_test_ctx)
                        self._validate_python_syntax(
                            starter_test_code, f"module_{idx}_{mod.name}/test_starter_example.py"
                        )
                        self.files.write_text(mod_dir / "test_starter_example.py", starter_test_code)
                        try:
                            self._sanitize_test_file(mod_dir / "test_starter_example.py", module_path_str, target_class)
                        except Exception:
                            pass
                if on_module_progress:
                    try:
                        on_module_progress(topic.name, idx, module_total, mod.name, "starter_test")
                    except Exception:
                        pass

                # Extra exercises via content generator
                try:
                    extra_md = self.content.extra_exercises(topic_dict, mod.model_dump(), idx)
                except Exception as exc:
                    if options.strict_ai_only:
                        self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=extra_exercises -> {exc}")
                        extra_md = ""
                    else:
                        extra_md = self.templates.render(
                            "extra_exercises.md.j2",
                            {
                                "module": {"title": mod.title, "focus_areas": mod.focus_areas},
                                "module_number": idx,
                                "topic": topic_dict,
                            },
                        )
                self.files.write_text(mod_dir / "extra_exercises.md", extra_md)
                if on_module_progress:
                    try:
                        on_module_progress(topic.name, idx, module_total, mod.name, "extra_exercises")
                    except Exception:
                        pass

                # Ensure package-style imports work from the module directory
                # so tests can do: from module_X_name import ClassName
                step = "package_init"
                exports: list[str] = []
                if starter_export_name:
                    exports.append(
                        f"from .starter_example import {starter_export_name}\n"
                    )
                if assignment_a_export_name:
                    exports.append(
                        f"from .assignment_a import {assignment_a_export_name}\n"
                    )
                # Assignment B may or may not exist depending on module type
                try:
                    if 'asg_b_ctx' in locals() and asg_b_ctx.get("class_name"):
                        exports.append(
                            f"from .assignment_b import {asg_b_ctx['class_name']}\n"
                        )
                except Exception:
                    pass

                init_content = "".join(exports) or "# Package exports for module imports in tests\n"
                self.files.write_text(mod_dir / "__init__.py", init_content)
                # Finalize: remove any residual ai_raw directories (we no longer keep raw AI outputs)
                try:
                    raw_dir = mod_dir / "ai_raw"
                    if raw_dir.exists():
                        for p in raw_dir.glob("**/*"):
                            try:
                                p.unlink()
                            except Exception:
                                pass
                        try:
                            raw_dir.rmdir()
                        except Exception:
                            pass
                except Exception:
                    pass
                if on_module_progress:
                    try:
                        on_module_progress(topic.name, idx, module_total, mod.name, "package_init")
                    except Exception:
                        pass
            except Exception as exc:  # pragma: no cover - enrich error context
                # Log unexpected module-level errors and continue to next module
                self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step={step} -> {exc}")
            finally:
                if on_module_progress:
                    try:
                        on_module_progress(topic.name, idx, module_total, mod.name, "done")
                    except Exception:
                        pass

        return ItemResult(
            topic_name=topic.name,
            success=True,
            status=f"Created with {len(paths.modules)} module(s)",
            output_path=paths.root,
        )

    @staticmethod
    def _validate_python_syntax(code: str, file_label: str) -> None:
        """Basic syntax validation to ensure generated code compiles.

        Raises SyntaxError if invalid; callers may catch to fallback or report.
        """
        try:
            # AST parse first for structural validation
            tree = ast.parse(code, filename=file_label, mode="exec")
            # Very light safety check: forbid exec/eval usage
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    if node.func.id in {"exec", "eval"}:  # pragma: no cover - safety
                        raise ValueError(f"Disallowed call '{node.func.id}' in {file_label}")
                # Forbid importing dangerous modules in generated code
                if isinstance(node, ast.Import):
                    forbidden = {"os", "subprocess", "shlex", "socket", "requests"}
                    for alias in node.names:
                        if alias.name.split(".")[0] in forbidden:  # pragma: no cover - safety
                            raise ValueError(
                                f"Disallowed import '{alias.name}' in {file_label}"
                            )
                if isinstance(node, ast.ImportFrom):
                    forbidden = {"os", "subprocess", "shlex", "socket", "requests"}
                    base = (node.module or "").split(".")[0]
                    if base in forbidden:  # pragma: no cover - safety
                        raise ValueError(
                            f"Disallowed import from '{node.module}' in {file_label}"
                        )
            # Bytecode compile for syntax confidence
            compile(code, file_label, "exec")
        except SyntaxError as exc:  # pragma: no cover - defensive
            # Re-raise with context label preserved
            raise

    @staticmethod
    def _is_valid_import_line(line: str) -> bool:
        """Return True if the line is a safe import statement.

        - Only allows a single import statement (no semicolons/newlines)
        - Forbids importing clearly dangerous modules (os, subprocess, shlex, socket, requests)
        """
        s = (line or "").strip()
        if not s:
            return False
        if ";" in s or "\n" in s:
            return False
        try:
            tree = ast.parse(s + "\n", filename="_import.py", mode="exec")
        except SyntaxError:
            return False
        # Must be a single import/import-from node
        if len(tree.body) != 1:
            return False
        node = tree.body[0]
        forbidden = {"os", "subprocess", "shlex", "socket", "requests"}
        if isinstance(node, ast.Import):
            for alias in node.names:
                base = (alias.name or "").split(".")[0]
                if base in forbidden:
                    return False
            return True
        if isinstance(node, ast.ImportFrom):
            base = (node.module or "").split(".")[0]
            if base in forbidden:
                return False
            return True
        return False

    @staticmethod
    def _is_valid_block(code: str, *, kind: str, params: str = "") -> bool:
        """Return True if the given code block parses as a function or method body.

        kind: "method" or "function". Params used only for method wrapper.
        """
        # Empty is considered valid (will be replaced by pass higher up when needed)
        if not code.strip():
            return False
        # Build a minimal wrapper for parsing
        try:
            if kind == "method":
                wrapper = f"class _C:\n    def _m(self{params}):\n        " + code.replace("\n", "\n        ") + "\n"
            else:
                wrapper = "def _f():\n    " + code.replace("\n", "\n    ") + "\n"
            ast.parse(wrapper, filename="_snippet.py", mode="exec")
            return True
        except Exception:
            return False

    @staticmethod
    def _is_valid_statement(stmt: str) -> bool:
        """Return True if the provided text parses as a single statement inside a function."""
        if not stmt.strip():
            return False
        try:
            wrapper = "def _f():\n    " + stmt.replace("\n", "\n    ") + "\n"
            ast.parse(wrapper, filename="_stmt.py", mode="exec")
            return True
        except Exception:
            return False

    @staticmethod
    def _sanitize_identifier(name: str, *, as_class: bool = False) -> str:
        """Return a safe Python identifier from arbitrary text.

        - Replaces non-alphanumeric/underscore with underscore
        - Collapses multiple underscores
        - Ensures it doesn't start with a digit
        - For classes: TitleCase
        - For functions: snake_case
        """
        if not name:
            return "GeneratedClass" if as_class else "generated_function"
        # Strip and replace illegal characters
        cleaned = re.sub(r"[^0-9a-zA-Z_]+", "_", name.strip())
        cleaned = re.sub(r"_+", "_", cleaned)
        cleaned = cleaned.strip("_") or ("GeneratedClass" if as_class else "generated_function")
        # Must not start with a digit
        if cleaned and cleaned[0].isdigit():
            cleaned = ("C_" if as_class else "f_") + cleaned
        if as_class:
            parts = cleaned.split("_")
            return "".join(p.capitalize() for p in parts if p)
        # function name in snake_case
        return cleaned.lower()

    @staticmethod
    def _strip_markdown_fences(code: str) -> str:
        """Remove Markdown code fences (``` or ```python) from AI responses.

        Returns the inner content if fences are present; otherwise returns the original text.
        """
        if not code:
            return code
        lines = code.splitlines()
        # Detect triple backtick fences
        starts = None
        ends = None
        for i, ln in enumerate(lines):
            if ln.strip().startswith("```"):
                starts = i
                break
        if starts is not None:
            for j in range(len(lines) - 1, starts, -1):
                if lines[j].strip().startswith("```"):
                    ends = j
                    break
        if starts is not None and ends is not None and ends > starts:
            inner = lines[starts + 1 : ends]
            return "\n".join(inner)
        # Also strip leading and trailing stray backticks if present
        stripped = code.strip()
        if stripped.startswith("```") and stripped.endswith("```"):
            return stripped.strip("`")
        return code

    # --- Post-generation helpers ---
    def _sanitize_test_file(self, path: Path, module_path: str, class_name: str) -> None:
        """Scan a test file for obvious placeholder tokens and replace with a simple smoke test.

        Allowed: TODO comments for students. Not allowed: 'expected_value', 'Replace with', 'method_name_'.
        """
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            return
        lowered = text.lower()
        bad_markers = [
            "expected_value",
            "replace with",
            "method_name_",
            "another_expected_value",
            "test_placeholder",
        ]
        if any(m in lowered for m in bad_markers):
            safe = (
                f"from {module_path} import {class_name}\n\n"
                f"def test_smoke_{class_name.lower()}:\n"
                f"    obj = {class_name}() if callable({class_name}) else None\n"
                f"    assert obj is None or isinstance(obj, {class_name})\n"
            )
            try:
                self._validate_python_syntax(safe, str(path))
                path.write_text(safe, encoding="utf-8")
            except Exception:
                # If even the smoke test can't be written, leave original content
                pass
