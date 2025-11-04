#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from lesson_generator.core.template_extractor import extract_to_temp
from lesson_generator.core.generator import LessonGenerator, GenerationOptions
from lesson_generator.core.topic_processor import TopicProcessor
from lesson_generator.content import FallbackContentGenerator


def main() -> None:
    reference = REPO.parent / "defensive_programming_lesson"
    if not reference.exists():
        raise SystemExit(f"Reference folder not found: {reference}")

    print(f"Extracting templates from: {reference}")
    templates_dir = extract_to_temp(reference)
    print(f"Templates extracted to: {templates_dir}")

    # Build a minimal topic via processor convenience
    topics = TopicProcessor().from_names(["extracted_course"])
    payload = json.dumps([t.model_dump() for t in topics])

    outdir = Path("/tmp/extracted_out")
    outdir.mkdir(parents=True, exist_ok=True)

    gen = LessonGenerator(templates_dir=templates_dir, content_generator=FallbackContentGenerator())
    res = gen.generate(topics=None, topics_json=payload, options=GenerationOptions(output_dir=outdir))

    for item in res.items:
        print(f"Generated: {item.topic_name} -> {item.output_path} ({item.status})")


if __name__ == "__main__":
    main()
