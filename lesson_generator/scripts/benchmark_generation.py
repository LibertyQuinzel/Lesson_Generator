#!/usr/bin/env python3
"""
Benchmark lesson generation time across different worker counts and topic sizes.

Usage:
  python scripts/benchmark_generation.py --topics 10 --workers 1 2 4 8 --output /tmp/bench_out
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
import sys

# Ensure local package imports work when running directly from repo
REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from lesson_generator.core.generator import LessonGenerator, GenerationOptions
from lesson_generator.core.topic_processor import ModuleModel, TopicModel
from lesson_generator.content import FallbackContentGenerator


def make_topics(n: int) -> list[TopicModel]:
    topics = []
    for i in range(1, n + 1):
        topics.append(
            TopicModel(
                name=f"topic_{i}",
                title=f"Topic {i}",
                description="Bench topic",
                difficulty="intermediate",
                estimated_hours=2,
                learning_objectives=["understand"],
                key_concepts=["kc"],
                modules=[
                    ModuleModel(
                        name="basics",
                        title="Basics",
                        type="starter",
                        focus_areas=["fa"],
                        complexity="simple",
                        estimated_time=30,
                    )
                ],
            )
        )
    return topics


def run_once(count: int, workers: int, outdir: Path) -> float:
    gen = LessonGenerator(content_generator=FallbackContentGenerator())
    payload = json.dumps([t.model_dump() for t in make_topics(count)])
    start = time.time()
    res = gen.generate(
        topics=None,
        topics_json=payload,
        options=GenerationOptions(output_dir=outdir, dry_run=False, workers=workers),
    )
    duration = time.time() - start
    ok = sum(1 for i in res.items if i.success)
    print(f"topics={count} workers={workers} duration={duration:.3f}s success={ok}/{len(res.items)}")
    return duration


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--topics", type=int, default=5)
    p.add_argument("--workers", type=int, nargs="+", default=[1, 2, 4])
    p.add_argument("--output", type=Path, default=Path("/tmp/lesson_bench"))
    args = p.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    for w in args.workers:
        run_once(args.topics, w, args.output)


if __name__ == "__main__":
    main()
