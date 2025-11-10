"""Lesson generation orchestrator.

This module is responsible for orchestrating the generation of complete lesson structures
including folder hierarchies, content files, and supporting materials. It works with:
- Topics: High-level subject areas (e.g., "async programming")
- Modules: Subdivisions of topics focusing on specific aspects
- Content: Generated lesson materials (examples, tests, documentation)
- Templates: Jinja2 templates for generating consistent file structures

Key responsibilities:
- Topic processing and validation
- Content generation and orchestration
- File structure management
- Template rendering and output generation
"""
from __future__ import annotations

import ast
import json
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import (
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Any,
    Tuple,
)

# Local imports from core functionality
from lesson_generator.core.file_manager import FileStructureManager
from lesson_generator.core.template_engine import TemplateEngine
from lesson_generator.core.topic_processor import (
    TopicModel,
    TopicProcessor,
    ModuleModel,
    ResourcesModel,
)
from lesson_generator.content import ContentGenerator


@dataclass
class GenerationOptions:
    """Options controlling lesson generation behavior.
    
    Attributes:
        output_dir: Directory where generated lessons will be written
        modules_override: Optional count to override number of modules per topic
        dry_run: If True, validate but don't write files
        workers: Number of parallel workers for generation (1 = sequential)
        difficulty_override: Optional difficulty level to apply to all topics
        strict_ai_only: If True, fail on AI errors rather than using fallbacks
        lessons_count: Optional limit on number of lessons to generate
        ai_direct_code: Generate code directly without template step
    """
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
    """Result of generating a single topic.
    
    Attributes:
        topic_name: Name of the topic that was generated
        success: Whether generation completed successfully
        status: Human-readable status message
        output_path: Path where generated content was written (None if failed)
    """
    topic_name: str
    success: bool
    status: str
    output_path: Optional[Path] = None


@dataclass
class GenerationResult:
    """Collection of results from generating multiple topics.
    
    Attributes:
        items: List of results for each topic that was processed
    """
    items: List[ItemResult]


class LessonGenerator:
    """Main orchestrator for generating lessons (Sprint 1 scope)."""

    def __init__(self, templates_dir: Optional[Path] = None, content_generator: ContentGenerator | None = None) -> None:
        """Initialize the lesson generator.
        
        Args:
            templates_dir: Path to templates directory. If None, uses default templates.
            content_generator: Generator for lesson content. Required.
            
        Raises:
            ValueError: If content_generator is None, wrong type, or templates_dir is invalid
            OSError: If templates directory cannot be accessed
            ImportError: If required modules cannot be imported
            RuntimeError: If initialization fails for other reasons
        """
        # Validate content generator
        if content_generator is None:
            raise ValueError("A content generator must be provided")
        if not hasattr(content_generator, 'plan_modules') or not hasattr(content_generator, 'starter_example'):
            raise ValueError(
                "Invalid content generator: must implement plan_modules() and starter_example()"
            )
        
        # Validate and resolve templates directory
        try:
            if templates_dir is None:
                templates_dir = Path(__file__).resolve().parents[1] / "templates"
            templates_dir = Path(templates_dir).resolve()
            
            if not templates_dir.exists():
                raise ValueError(f"Templates directory does not exist: {templates_dir}")
            if not templates_dir.is_dir():
                raise ValueError(f"Templates path is not a directory: {templates_dir}")
            if not any(templates_dir.iterdir()):
                raise ValueError(f"Templates directory is empty: {templates_dir}")
        except (TypeError, ValueError) as e:
            raise ValueError(f"Invalid templates directory path: {e}") from e
        except OSError as e:
            raise OSError(f"Cannot access templates directory {templates_dir}: {e}") from e
            
        # Initialize components
        try:
            self.templates = TemplateEngine(templates_dir)
            self.files = FileStructureManager()
            self.topics = TopicProcessor()
            self.content = content_generator
        except ImportError as e:
            raise ImportError(f"Failed to import required module: {e}") from e
        except OSError as e:
            raise OSError(f"Failed to initialize file system components: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Failed to initialize lesson generator: {e}") from e

    # Append error messages to a per-topic errors.txt without interrupting generation
    @staticmethod
    def _append_error(error_file: Path, message: str) -> None:
        try:
            error_file.parent.mkdir(parents=True, exist_ok=True)
            with error_file.open("a", encoding="utf-8") as f:
                f.write(str(message).rstrip() + "\n")
        except OSError as e:
            # Don't let logging issues break generation, but log to stderr for debugging
            import sys
            print(f"Warning: Could not write to error file {error_file}: {e}", file=sys.stderr)

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
        # Build topic models from both JSON config and topic names
        topic_models: List[TopicModel] = []
        models_from_config: List[TopicModel] = []
        models_from_names: List[TopicModel] = []
        
        # Parse topics from JSON configuration if provided
        if topics_json:
            if not isinstance(topics_json, str):
                raise TypeError(f"topics_json must be a string, got {type(topics_json)}")
            try:
                models_from_config = self.topics.parse_topics(topics_json)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format in topics_json: {e}")
            except KeyError as e:
                raise ValueError(f"Missing required field in topics_json: {e}")
            topic_models.extend(models_from_config)
            
        # Create topics from names if provided
        if topics:
            if not isinstance(topics, (list, tuple, set)):
                topics = list(topics)  # Convert other iterables to list
            if not topics:
                raise ValueError("topics iterable is empty")
            if any(not isinstance(t, str) for t in topics):
                raise TypeError("All topics must be strings")
                
            try:
                models_from_names = self.topics.from_names(list(topics))
            except ValueError as e:
                raise ValueError(f"Invalid topic name: {e}")
            topic_models.extend(models_from_names)

        # For topics provided as names, generate module structure using AI or fallback
        if models_from_names:
            if not isinstance(options.modules_override, (int, type(None))):
                raise ValueError(
                    f"modules_override must be an integer or None, got {type(options.modules_override)}"
                )
                
            desired_count = int(options.modules_override or 5)
            if desired_count < 1:
                raise ValueError(f"modules_override must be positive, got {desired_count}")
                
            for t in models_from_names:
                if not t.name:
                    raise ValueError("Topic name cannot be empty")
                    
                try:
                    plan = self.content.plan_modules(t.name, desired_count)
                except ValueError as e:
                    raise ValueError(f"Invalid module count for topic '{t.name}': {e}")
                except (KeyError, TypeError) as e:
                    raise RuntimeError(f"Invalid module plan format for topic '{t.name}': {e}")
                except Exception as exc:
                    if options.strict_ai_only and not options.dry_run:
                        # Respect strict AI requirement when actually generating files
                        raise RuntimeError(
                            f"AI module planning failed for topic '{t.name}': {exc}"
                        ) from exc
                    # In non-strict mode, error will be logged and fallback used
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
                            # No fallback - continue with next step
                            continue
                    except Exception as exc:
                        self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=starter_example -> {exc}")
                        continue
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
                            continue
                except Exception as exc:
                    self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=assignment_a -> {exc}")
                    # Create a minimal, non-placeholder assignment to ensure the file exists
                    try:
                        placeholder_class = self._sanitize_identifier(
                            f"{mod.name.title().replace('_','')}AssignmentA",
                            as_class=True
                        )
                        docstring = (
                            "Auto-generated assignment A fallback.\n"
                            "TODO: Implement the business logic as described in the module README."
                        )
                        placeholder = '\n'.join([
                            f'"""{docstring}"""',
                            "",
                            f"class {placeholder_class}:",
                            "    def process(self, data=None):",
                            '        """TODO: replace this with a real implementation.',
                            "",
                            "        This minimal method returns 0 to keep tests importable.",
                            '        """',
                            "        return 0",
                            "",
                        ])
                        self.files.write_text(mod_dir / "assignment_a.py", placeholder)
                        assignment_a_export_name = placeholder_class
                        asg_a_ctx = {
                            "class_name": placeholder_class,
                            "description": "Assignment A",
                            "variant": "a",
                            "source_code": placeholder
                        }
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
                    # If tests are templates, add multiple skeleton tests and detailed instructions
                    try:
                        if tests_a_ctx.get("is_template"):
                            tests_a_ctx.setdefault(
                                "test_instructions",
                                (
                                    "Write focused pytest tests for the assignment below.\n"
                                    "Each test should follow GIVEN / WHEN / THEN structure.\n"
                                    "Provide at least: one happy-path test, one edge-case test, one error/validation test,\n"
                                    "and one additional behavioural/contract test (4 tests minimum).\n"
                                    "Replace the placeholder assertions with concrete expectations from the module README."
                                ),
                            )
                            cls = (
                                tests_a_ctx.get("class_name")
                                or (asg_a_ctx.get("class_name") if isinstance(asg_a_ctx, dict) else None)
                                or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentA", as_class=True)
                            )
                            tests_a_ctx.setdefault("test_methods", [])
                            # Ensure at least 4 skeleton tests are present
                            while len(tests_a_ctx["test_methods"]) < 4:
                                idx_stub = len(tests_a_ctx["test_methods"]) + 1
                                if idx_stub == 1:
                                    tests_a_ctx["test_methods"].append(
                                        {
                                            "name": "happy_path",
                                            "description": "Happy path: basic expected behaviour",
                                            "given_section": f"obj = {cls}()",
                                            "when_section": "# TODO: call the method under test, e.g. result = obj.method(args)",
                                            "then_section": "assert False, \"TODO: replace with expected assertion for happy path\"",
                                        }
                                    )
                                elif idx_stub == 2:
                                    tests_a_ctx["test_methods"].append(
                                        {
                                            "name": "edge_case_input",
                                            "description": "Edge case: invalid or boundary input",
                                            "given_section": f"obj = {cls}()",
                                            "when_section": "# TODO: call the method with an edge-case input",
                                            "then_section": "assert False, \"TODO: implement edge-case assertion\"",
                                        }
                                    )
                                else:
                                    tests_a_ctx["test_methods"].append(
                                        {
                                            "name": "error_handling",
                                            "description": "Validation / error handling expectations",
                                            "given_section": f"obj = {cls}()",
                                            "when_section": "# TODO: call the method in a way that triggers error handling",
                                            "then_section": "assert False, \"TODO: assert expected exception or error message\"",
                                        }
                                    )
                    except Exception:
                        pass
                    # Use assignment-A-specific template to produce a student-facing test template
                    test_a_code = self.templates.render("test_assignment_a.py.j2", tests_a_ctx)
                    # Remove any Markdown code fences that may have been introduced by AI content
                    try:
                        test_a_code = self._strip_markdown_fences(test_a_code).lstrip()
                    except Exception:
                        pass
                    # Ensure we don't write empty/blank test files; provide a helpful skeleton
                    if not (test_a_code and test_a_code.strip()):
                        test_a_code = (
                            '"""\\n'
                            'Auto-generated test skeleton for Assignment A.\\n'
                            'Students: replace the TODOs below with concrete tests to reach 100% coverage.\\n'
                            '"""\\n\\n'
                            'def test_happy_path_should_pass():\\n'
                            '    """Happy-path: implement and assert expected behaviour."""\\n'
                            '    # TODO: create instance and call method under test\\n'
                            '    # e.g. obj = MyClass(); result = obj.method(arg)\\n'
                            '    assert False, "TODO: replace with expected assertion for happy path"\\n\\n'
                            'def test_edge_case_should_be_handled():\\n'
                            '    """Edge-case: test invalid or boundary inputs."""\\n'
                            '    # TODO: call the method with edge-case input and assert expected handling\\n'
                            '    assert False, "TODO: implement edge-case assertion"\\n\\n'
                            'def test_error_handling_raises_or_returns():\\n'
                            '    """Error handling: ensure validation or exceptions behave as documented."""\\n'
                            '    # TODO: call the method in a way that triggers error handling and assert expected exception or message\\n'
                            '    assert False, "TODO: assert expected exception or error message"\\n\\n'
                            'def test_additional_contracts_and_behaviour():\\n'
                            '    """Additional behavioural/contract tests - exercise less common flows."""\\n'
                            '    # TODO: add another focused test (e.g. state change, return type, or side-effects)\\n'
                            '    assert False, "TODO: implement additional behavioural assertion"\\n'
                        )
                    try:
                        self._validate_python_syntax(test_a_code, f"module_{idx}_{mod.name}/test_assignment_a.py")
                        self.files.write_text(mod_dir / "test_assignment_a.py", test_a_code)
                        # Only sanitize if this is NOT a template test (templates should have placeholder content)
                        is_template_test = tests_a_ctx.get("is_template", False)
                        if not is_template_test:
                            try:
                                self._sanitize_test_file(mod_dir / "test_assignment_a.py", f"module_{idx}_{mod.name}", assignment_a_export_name or (asg_a_ctx.get("class_name") if isinstance(asg_a_ctx, dict) else None) or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentA", as_class=True))
                            except Exception:
                                pass
                    except Exception:
                        if options.strict_ai_only:
                            raise
                        continue
                except Exception as exc:
                    self._append_error(errors_file, f"[{topic.name}] module {idx}:{mod.name} step=tests_a -> {exc}")
                    # Write a simple, non-placeholder smoke test to ensure presence
                    try:
                        cls = assignment_a_export_name or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentA", as_class=True)
                        module_path_str = f"module_{idx}_{mod.name}"
                        smoke = (
                            f"from {module_path_str} import {cls}\n\n"
                            f"def test_assignment_a_happy_path():\n"
                            f"    \"\"\"Happy-path: implement and assert expected behaviour.\"\"\"\n"
                            f"    obj = {cls}()\n"
                            f"    # TODO: call a representative method or check a default state\n"
                            f"    assert False, 'TODO: replace with expected assertion for happy path'\n\n"
                            f"def test_assignment_a_edge_case():\n"
                            f"    \"\"\"Edge-case: invalid or boundary input - implement and assert expected behaviour.\"\"\"\n"
                            f"    obj = {cls}()\n"
                            f"    # TODO: exercise an edge case and assert expected behaviour\n"
                            f"    assert False, 'TODO: implement edge-case assertion'\n\n"
                            f"def test_assignment_a_error_handling():\n"
                            f"    \"\"\"Error handling: ensure validation or exceptions behave as documented.\"\"\"\n"
                            f"    obj = {cls}()\n"
                            f"    # TODO: call a method in a way that triggers error handling and assert expected exception or message\n"
                            f"    assert False, 'TODO: assert expected exception or error message'\n\n"
                            f"def test_assignment_a_additional_contracts():\n"
                            f"    \"\"\"Additional behavioural/contract tests - exercise less common flows.\"\"\"\n"
                            f"    obj = {cls}()\n"
                            f"    # TODO: add another focused test (e.g. state change, return type, or side-effects)\n"
                            f"    assert False, 'TODO: implement additional behavioural assertion'\n"
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

                                    # Regardless of whether AI returned a complete implementation,
                                    # replace the implementation with a student-facing scaffold:
                                    # extract method names/signatures and write a class where
                                    # each method raises NotImplementedError so students must
                                    # implement them.
                                    try:
                                        cls_node = None
                                        for n in tree_b.body:
                                            if isinstance(n, ast.ClassDef):
                                                cls_node = n
                                                break
                                        methods_list = []
                                        if cls_node is not None:
                                            for item in cls_node.body:
                                                if isinstance(item, ast.FunctionDef):
                                                    # gather parameter names excluding self
                                                    params = []
                                                    for a in item.args.args:
                                                        if a.arg != "self":
                                                            params.append(a.arg)
                                                    param_str = ", ".join(params)
                                                    methods_list.append({
                                                        "name": item.name,
                                                        "parameters": (", " + param_str) if param_str else "",
                                                    })
                                        # If AI did not provide methods, ensure a default method scaffold
                                        if not methods_list:
                                            methods_list = [{"name": "process", "parameters": ""}, {"name": "execute", "parameters": ""}, {"name": "attach_observer", "parameters": ", observer"}]

                                        # Build scaffold class source: keep class name but replace bodies
                                        scaffold_lines = [f'"""\nAuto-generated scaffold for Assignment B.\nStudents must implement the methods below to make tests in test_assignment_b.py pass.\n"""', "", f"class {inferred_b}:", "    def __init__(self):", "        \"\"\"Initialise any internal state required by the implementation.\"\"\"", "        pass", ""]
                                        for m in methods_list:
                                            # Normalize parameters for definition (strip leading comma/space)
                                            params = (m.get("parameters") or "").lstrip()
                                            if params.startswith(","):
                                                params = params[1:].lstrip()
                                            sig = f"def {m['name']}(self" + (", " + params if params else "") + "):" 
                                            scaffold_lines.append(f"    {sig}")
                                            scaffold_lines.append("        \"\"\"TODO: implement this method to satisfy tests in test_assignment_b.py\"\"\"")
                                            scaffold_lines.append("        raise NotImplementedError(\"TODO: implement\")")
                                            scaffold_lines.append("")

                                        scaffold_code = "\n".join(scaffold_lines)
                                        # validate and write scaffold as assignment_b.py
                                        try:
                                            self._validate_python_syntax(scaffold_code, f"module_{idx}_{mod.name}/assignment_b.py")
                                            self.files.write_text(mod_dir / "assignment_b.py", scaffold_code)
                                            asg_b_ctx = {
                                                "class_name": inferred_b,
                                                "description": "Assignment B (student scaffold)",
                                                "variant": "b",
                                                "source_code": scaffold_code,
                                                "methods": methods_list,
                                            }
                                        except Exception:
                                            # If scaffold validation fails, fall back to storing raw AI output
                                            asg_b_ctx = {"class_name": inferred_b, "description": "Assignment B", "variant": "b", "source_code": code_text_b}
                                    except Exception:
                                        # On any extraction error, keep raw AI output but ensure downstream code has a class_name
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
                            # Convert assignment B into a student-implementation scaffold: ensure method bodies are TODO stubs
                            try:
                                methods = asg_b_ctx.get("methods") or []
                                if not methods:
                                    methods = [
                                        {
                                            "name": "process",
                                            "parameters": "",
                                            "args": [],
                                            "docstring": "TODO: implement process to satisfy tests in test_assignment_b.py",
                                            "implementation": (
                                                '"""TODO: Implement this method so the provided tests pass.\n'
                                                'Instructions: Read the module README and tests to implement expected behaviour.\n'
                                                '"""\n'
                                                'raise NotImplementedError("TODO: implement")'
                                            ),
                                            "return_type": "Any",
                                            "return_description": "",
                                        }
                                    ]
                                else:
                                    for m in methods:
                                        try:
                                            m["implementation"] = (
                                                '"""TODO: Implement this method so the provided tests in test_assignment_b.py pass.\n'
                                                'Instructions: follow the module README and tests for expected behaviour.\n'
                                                '"""\n'
                                                'raise NotImplementedError("TODO: implement")'
                                            )
                                        except Exception:
                                            pass
                                asg_b_ctx["methods"] = methods
                            except Exception:
                                pass
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
                                continue
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
                        tests_b_ctx = self.content.tests_for_assignment(topic_dict, mod_ctx, asg_b_ctx) or {}
                        # Align test class target with exported class name
                        if asg_b_ctx.get("class_name"):
                            tests_b_ctx["class_name"] = asg_b_ctx["class_name"]
                            tests_b_ctx["test_target_name"] = asg_b_ctx["class_name"]
                        # Force concrete (non-template) tests for Assignment B so students
                        # always receive runnable test suites rather than an empty placeholder.
                        tests_b_ctx["is_template"] = False
                        # Ensure there's a test_methods list we can pad if AI didn't provide enough
                        tests_b_ctx.setdefault("test_methods", [])
                        try:
                            # Prefer method names discovered in the assignment scaffold
                            methods = [m.get("name") for m in (asg_b_ctx.get("methods") or []) if isinstance(m, dict) and m.get("name")]
                        except Exception:
                            methods = []
                        # Fill names to try to create at least 4 distinct tests
                        fill_names = (methods or ["process", "execute", "attach_observer", "configure"])[:4]
                        # Append placeholder behavioural tests until we have 4
                        while len(tests_b_ctx["test_methods"]) < 4:
                            idx_fill = len(tests_b_ctx["test_methods"]) + 1
                            mname = fill_names[(idx_fill - 1) % len(fill_names)]
                            if mname.lower().startswith("attach"):
                                when = f"obj.{mname}('observer')"
                                then = "assert True  # TODO: assert observer was registered (check internal state or returned value)"
                            elif mname.lower().startswith("create") or mname.lower().startswith("execute"):
                                when = f"result = obj.{mname}('sample')"
                                then = "assert isinstance(result, str) and result, \"Expected a non-empty descriptive string\""
                            else:
                                when = f"result = obj.{mname}()"
                                then = "assert result is not None  # TODO: replace with concrete expectation"
                            tests_b_ctx["test_methods"].append(
                                {
                                    "name": f"{mname}_behaviour_{len(tests_b_ctx['test_methods'])+1}",
                                    "description": f"Behavioural test for {mname}",
                                    "given_section": f"obj = {tests_b_ctx.get('class_name') or self._sanitize_identifier(f'{mod.name.title().replace('_','')}AssignmentB', as_class=True)}()",
                                    "when_section": when,
                                    "then_section": then,
                                }
                            )
                        # Force correct module import path for reliability
                        try:
                            module_path_str = f"module_{idx}_{mod.name}"
                            tests_b_ctx["module_path"] = module_path_str
                        except Exception:
                            pass
                        # Ensure tests for assignment B include multiple checks and detailed instructions
                        try:
                            tests_b_ctx.setdefault(
                                "test_instructions",
                                (
                                    "These are concrete tests that describe the expected behaviour for Assignment B.\n"
                                    "Students should implement the methods in assignment_b.py so these tests pass.\n"
                                    "Focus on return types, outputs and side-effects documented in the module README.\n"
                                ),
                            )
                            tests_b_ctx.setdefault("test_methods", [])
                            existing = tests_b_ctx.get("test_methods") or []
                            try:
                                methods = [m.get("name") for m in (asg_b_ctx.get("methods") or []) if isinstance(m, dict) and m.get("name")]
                            except Exception:
                                methods = []
                            fill_names = (methods or ["process", "execute", "attach_observer"])[:4]
                            idx_fill = 0
                            while len(existing) < 4:
                                mname = fill_names[idx_fill % len(fill_names)]
                                if mname.lower().startswith("attach"):
                                    when = f"obj.{mname}('observer')"
                                    then = "assert True  # TODO: assert observer was registered (check internal state or returned value)"
                                elif mname.lower().startswith("create") or mname.lower().startswith("execute"):
                                    when = f"result = obj.{mname}('sample')"
                                    then = "assert isinstance(result, str) and result, \"Expected a non-empty descriptive string\""
                                else:
                                    when = f"result = obj.{mname}()"
                                    then = "assert result is not None  # TODO: replace with concrete expectation"
                                existing.append(
                                    {
                                        "name": f"{mname}_behaviour",
                                        "description": f"Behavioural test for {mname}",
                                        "given_section": f"obj = {tests_b_ctx.get('class_name') or self._sanitize_identifier(f'{mod.name.title().replace('_','')}AssignmentB', as_class=True)}()",
                                        "when_section": when,
                                        "then_section": then,
                                    }
                                )
                                idx_fill += 1
                            tests_b_ctx["test_methods"] = existing
                        except Exception:
                            pass
                        # Use assignment-B-specific template which produces concrete, runnable tests
                        test_b_code = self.templates.render("test_assignment_b.py.j2", tests_b_ctx)
                        try:
                            test_b_code = self._strip_markdown_fences(test_b_code).lstrip()
                        except Exception:
                            pass
                        # Ensure we don't write empty/blank test files; provide a clear placeholder
                        if not (test_b_code and test_b_code.strip()):
                            # Attempt to produce a concrete test suite for a SimpleList-style assignment
                            module_path = tests_b_ctx.get("module_path") or f"module_{idx}_{mod.name}"
                            cls_name = tests_b_ctx.get("class_name") or (asg_b_ctx.get("class_name") if isinstance(asg_b_ctx, dict) else None) or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentB", as_class=True)
                            test_b_code = (
                                '"""\n'
                                'Auto-generated tests for Assignment B.\n'
                                'These tests assume a SimpleList-like API with: __init__(max_capacity), add(item), remove_last(), get(index), size (property), is_full (property).\n'
                                'Students should implement the class to satisfy these behaviours.\n'
                                '"""\n\n'
                                f'from {module_path} import {cls_name}\n\n'
                                'def test_init_size_and_is_full():\n'
                                f'    lst = {cls_name}(3)\n'
                                '    assert lst.size == 0\n'
                                '    assert not lst.is_full\n\n'
                                'def test_add_until_full_and_return_values():\n'
                                f'    lst = {cls_name}(2)\n'
                                '    assert lst.add("a") is True\n'
                                '    assert lst.size == 1\n'
                                '    assert lst.add("b") is True\n'
                                '    assert lst.size == 2\n'
                                '    assert lst.is_full is True\n'
                                '    assert lst.add("c") is False\n\n'
                                'def test_remove_last_and_get():\n'
                                f'    lst = {cls_name}(3)\n'
                                '    lst.add("x")\n'
                                '    lst.add("y")\n'
                                '    assert lst.remove_last() == "y"\n'
                                '    assert lst.size == 1\n'
                                '    assert lst.get(0) == "x"\n'
                                '    assert lst.get(1) is None\n'
                                '    assert lst.remove_last() == "x"\n'
                                '    assert lst.remove_last() is None\n\n'
                                'def test_get_invalid_index_returns_none():\n'
                                f'    lst = {cls_name}(1)\n'
                                '    assert lst.get(-1) is None\n'
                                '    assert lst.get(100) is None\n'
                            )
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
                            else:
                                continue
                                fb_tests_b["class_name"] = asg_b_ctx["class_name"]
                                fb_tests_b["test_target_name"] = asg_b_ctx["class_name"]
                            # Render fallback using the concrete Assignment B template as well
                            fb_test_b_code = self.templates.render("test_assignment_b.py.j2", fb_tests_b)
                            try:
                                fb_test_b_code = self._strip_markdown_fences(fb_test_b_code).lstrip()
                            except Exception:
                                pass
                            if not (fb_test_b_code and fb_test_b_code.strip()):
                                module_path = (asg_b_ctx.get("module_path") if isinstance(asg_b_ctx, dict) else None) or f"module_{idx}_{mod.name}"
                                cls_name = (asg_b_ctx.get("class_name") if isinstance(asg_b_ctx, dict) else None) or self._sanitize_identifier(f"{mod.name.title().replace('_','')}AssignmentB", as_class=True)
                                fb_test_b_code = (
                                    '"""\n'
                                    'Fallback tests for Assignment B.\n'
                                    'These tests assume a SimpleList-like API: __init__(max_capacity), add(item), remove_last(), get(index), size, is_full.\n'
                                    '"""\n\n'
                                    f'from {module_path} import {cls_name}\n\n'
                                    'def test_add_and_full_behaviour():\n'
                                    f'    lst = {cls_name}(2)\n'
                                    '    assert lst.add(1) is True\n'
                                    '    assert lst.add(2) is True\n'
                                    '    assert lst.add(3) is False\n\n'
                                    'def test_remove_last_and_size_updates():\n'
                                    f'    lst = {cls_name}(2)\n'
                                    '    lst.add("a")\n'
                                    '    lst.add("b")\n'
                                    '    assert lst.remove_last() == "b"\n'
                                    '    assert lst.size == 1\n'
                                )
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

                            # Extract methods from assignment_b.py for test generation
                            methods = []
                            try:
                                if isinstance(asg_b_ctx, dict) and asg_b_ctx.get("source_code"):
                                    import ast
                                    tree = ast.parse(asg_b_ctx["source_code"])
                                    methods = [node.name for node in ast.walk(tree) 
                                             if isinstance(node, ast.FunctionDef) and not node.name.startswith('_')]
                            except Exception:
                                pass

                            # If we couldn't extract methods, use a default set
                            if not methods:
                                methods = ["process", "validate", "transform", "execute"]

                            # Generate comprehensive test template
                            test_template = [
                                f"from {module_path_str} import {cls_b}",
                                "",
                                "import pytest",
                                "",
                                '"""',
                                "Comprehensive tests for Assignment B implementation.",
                                "Students must implement the class to satisfy these tests.",
                                '"""',
                                ""
                            ]

                            # Check if this is an iterator implementation
                            is_iterator = False
                            iterator_methods = set()
                            try:
                                if "source_code" in assignment_ctx:
                                    import ast
                                    tree = ast.parse(assignment_ctx["source_code"])
                                    for node in ast.walk(tree):
                                        if isinstance(node, ast.FunctionDef):
                                            if node.name in ['__iter__', '__next__']:
                                                is_iterator = True
                                            iterator_methods.add(node.name)
                            except Exception:
                                pass

                            if is_iterator:
                                # Generate iterator-specific tests
                                test_template.extend([
                                    "def test_iterator_protocol():",
                                    '    """Test basic iterator protocol implementation"""',
                                    "    # Test creation and iteration",
                                    f"    data = [1, 2, 3]",
                                    f"    iterator = {cls_b}(data)",
                                    "    assert list(iterator) == data",
                                    "",
                                    "def test_next_functionality():",
                                    '    """Test __next__ method behavior"""',
                                    "    # Test normal next() calls",
                                    f"    iterator = {cls_b}([1, 2])",
                                    "    assert next(iterator) == 1",
                                    "    assert next(iterator) == 2",
                                    "    ",
                                    "    # Test StopIteration",
                                    "    with pytest.raises(StopIteration):",
                                    "        next(iterator)",
                                    ""
                                ])

                                if 'reset' in iterator_methods:
                                    test_template.extend([
                                        "def test_reset_functionality():",
                                        '    """Test reset method"""',
                                        f"    iterator = {cls_b}([1, 2, 3])",
                                        "    # Consume some items",
                                        "    next(iterator)",
                                        "    next(iterator)",
                                        "    # Test reset",
                                        "    iterator.reset()",
                                        "    assert next(iterator) == 1  # Should start from beginning",
                                        ""
                                    ])

                                if 'has_next' in iterator_methods:
                                    test_template.extend([
                                        "def test_has_next_functionality():",
                                        '    """Test has_next method"""',
                                        f"    iterator = {cls_b}([1, 2])",
                                        "    assert iterator.has_next() is True",
                                        "    next(iterator)",
                                        "    assert iterator.has_next() is True",
                                        "    next(iterator)",
                                        "    assert iterator.has_next() is False",
                                        ""
                                    ])

                                # Add reusability test
                                test_template.extend([
                                    "def test_reuse_after_completion():",
                                    '    """Test iterator reuse after completion"""',
                                    "    data = [1, 2, 3]",
                                    f"    iterator = {cls_b}(data)",
                                    "    ",
                                    "    # First complete iteration",
                                    "    assert list(iterator) == data",
                                    "",
                                    "    # Reset and iterate again",
                                    "    iterator.reset()",
                                    "    assert list(iterator) == data",
                                    "",
                                    "def test_empty_iterator():",
                                    '    """Test behavior with empty data"""',
                                    f"    iterator = {cls_b}([])",
                                    "    assert iterator.has_next() is False",
                                    "    with pytest.raises(StopIteration):",
                                    "        next(iterator)",
                                    ""
                                ])
                            else:
                                # Original method-specific test generation for non-iterator classes
                                for method in methods[:2]:
                                    param_info = {"name": "value", "type": "Any"}  # Default
                                    try:
                                        if "source_code" in assignment_ctx:
                                            tree = ast.parse(assignment_ctx["source_code"])
                                            for node in ast.walk(tree):
                                                if isinstance(node, ast.FunctionDef) and node.name == method:
                                                    if node.args.args:
                                                        first_param = node.args.args[1]  # Skip self
                                                        param_info["name"] = first_param.arg
                                                        if hasattr(first_param, 'annotation'):
                                                            if isinstance(first_param.annotation, ast.Name):
                                                                param_info["type"] = first_param.annotation.id
                                    except Exception:
                                        pass

                                # Add happy path test
                                test_template.extend([
                                    f"def test_{method}_valid_inputs():",
                                    f'    """Test {method} with valid inputs"""',
                                    f"    obj = {cls_b}()",
                                    f"    # Test with valid inputs",
                                ])
                                
                                # Add type-specific test cases
                                if param_info["type"] in ["int", "float"]:
                                    test_template.extend([
                                        f"    obj.{method}(5)",
                                        f"    obj.{method}(1)",
                                        f"    obj.{method}(100)",
                                    ])
                                elif param_info["type"] == "str":
                                    test_template.extend([
                                        f'    obj.{method}("valid input")',
                                        f'    obj.{method}("a")',
                                        f'    obj.{method}("   spaces   ")',
                                    ])
                                else:
                                    test_template.extend([
                                        f"    result = obj.{method}(valid_input)",
                                        f"    assert result is not None",
                                    ])
                                
                                test_template.append("")

                                # Add error case test
                                test_template.extend([
                                    f"def test_{method}_error_handling():",
                                    f'    """Test {method} error handling"""',
                                    f"    obj = {cls_b}()",
                                    f"    with pytest.raises((ValueError, AssertionError)):",
                                ])
                                
                                # Add type-specific error cases
                                if param_info["type"] in ["int", "float"]:
                                    test_template.extend([
                                        f"        obj.{method}(-1)",
                                        f"        obj.{method}(0)",
                                    ])
                                elif param_info["type"] == "str":
                                    test_template.extend([
                                        f'        obj.{method}("")',
                                        f'        obj.{method}("   ")',
                                    ])
                                else:
                                    test_template.extend([
                                        f"        obj.{method}(None)",
                                        f"        obj.{method}(invalid_input)",
                                    ])
                                
                                test_template.append("")

                            # Add integration test if there are multiple methods
                            if len(methods) > 1:
                                test_template.extend([
                                    "def test_method_integration():",
                                    '    """Test integration between methods"""',
                                    f"    obj = {cls_b}()",
                                    "    # Test methods in combination",
                                    f"    obj.{methods[0]}(valid_input_1)",
                                    f"    obj.{methods[1]}(valid_input_2)",
                                    "    assert True  # Replace with actual integration test",
                                    ""
                                ])

                            # Join all lines with proper newlines
                            placeholder = "\n".join(test_template)
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
        # First, strip any leading/trailing Markdown code fences that AI sometimes returns
        stripped = text
        # Remove top-level triple-backtick fences (``` or ```python)
        lines = stripped.splitlines()
        if lines and lines[0].strip().startswith("```") and lines[-1].strip().startswith("```"):
            # Drop the first and last fence lines
            stripped = "\n".join(lines[1:-1])
        # Also defensively remove any remaining fenced blocks entirely if they enclose the whole file
        stripped = re.sub(r"^```(?:python)?\n|\n```$", "", stripped, flags=re.IGNORECASE)

        lowered = stripped.lower()
        bad_markers = [
            "expected_value",
            "replace with",
            "method_name_",
            "another_expected_value",
            "test_placeholder",
        ]
        if any(m in lowered for m in bad_markers):
            # Construct a minimal, valid smoke test. Ensure function name includes parentheses.
            safe = (
                f"from {module_path} import {class_name}\n\n"
                f"def test_smoke_{class_name.lower()}():\n"
                f"    obj = {class_name}() if callable({class_name}) else None\n"
                f"    assert obj is None or isinstance(obj, {class_name})\n"
            )
            try:
                self._validate_python_syntax(safe, str(path))
                path.write_text(safe, encoding="utf-8")
            except Exception:
                # If even the smoke test can't be written, leave original content
                pass
            return

        # If no bad markers, but the file still contains stray fences, write back the cleaned content
        if stripped != text:
            try:
                # final sanity check: ensure cleaned code compiles
                self._validate_python_syntax(stripped, str(path))
                path.write_text(stripped, encoding="utf-8")
            except Exception:
                # If cleaned content still doesn't pass validation, leave original
                pass
