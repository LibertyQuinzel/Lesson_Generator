# Performance and Benchmarks

This document describes how to measure lesson generation performance and how to interpret results.

## What we measure

- End-to-end generation time for a set of topics
- Impact of worker parallelism (`--workers`) on throughput
- Success ratio (generated items without validation errors)

## Quick benchmark

Use the helper script to run a simple benchmark locally:

- File: `scripts/benchmark_generation.py`
- Example: `python scripts/benchmark_generation.py --topics 20 --workers 1 2 4 8 --output /tmp/bench_out`

The script generates synthetic topics and runs the generator with the fallback content engine to avoid network variance.

Expected output lines (example):

```
topics=20 workers=1 duration=2.134s success=20/20
topics=20 workers=2 duration=1.212s success=20/20
topics=20 workers=4 duration=0.749s success=20/20
```

Notes:
- Parallel speedup depends on CPU, disk, and Python thread behavior; I/O-bound workloads generally benefit more.
- When using the OpenAI backend, network latency and rate limits dominate; the benchmark script intentionally uses the fallback generator for stable results.

## Tips

- Use a fast local disk for output directories.
- Increase `--workers` until you stop seeing benefits; too many can cause contention.
- Prefer batching multiple topics per run rather than many small runs to amortize startup costs.
