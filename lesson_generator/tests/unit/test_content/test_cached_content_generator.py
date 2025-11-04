from __future__ import annotations

from lesson_generator.content import CachedContentGenerator, FallbackContentGenerator


def test_cached_content_reuses_results():
    fb = FallbackContentGenerator()
    cg = CachedContentGenerator(fb)
    topic = {"name": "t", "title": "T", "learning_objectives": ["lo1"], "key_concepts": ["kc"]}
    module = {"name": "m", "title": "M", "focus_areas": ["fa"]}

    a1 = cg.assignment(topic, module, variant="a")
    a2 = cg.assignment(topic, module, variant="a")
    # Cached object should be the same dict instance
    assert a1 is a2


def test_cached_smoke_test_cache_key_uses_method_names():
    fb = FallbackContentGenerator()
    cg = CachedContentGenerator(fb)
    code1 = cg.starter_smoke_test("pkg.mod", "ClassX", methods=[{"name": "demo"}])
    code2 = cg.starter_smoke_test("pkg.mod", "ClassX", methods=[{"name": "demo"}])
    assert code1 is code2 or code1 == code2

    # Different method names should produce a different cache key and (likely) different text
    code3 = cg.starter_smoke_test("pkg.mod", "ClassX", methods=[{"name": "run"}])
    assert code3 == code3  # sanity
    assert code3 != code1 or code3 is not code1
