from lesson_generator.core.topic_processor import ModuleModel, TopicProcessor


def test_module_name_normalization_empty_and_punct():
    # Empty name -> prefix 'm'
    mod_empty = ModuleModel(name="", title="T", type="starter", focus_areas=["fa"])
    assert mod_empty.name == "m"

    # Punctuation only -> cleaned to empty then prefixed
    mod_punct = ModuleModel(name="!!!", title="T", type="starter", focus_areas=["fa"])
    assert mod_punct.name == "m"


def test_from_names_title_fallback_for_blank():
    tp = TopicProcessor()
    topics = tp.from_names(["   "])  # whitespace becomes empty after strip
    assert topics[0].title == "Lesson"
    # Topic name is normalized to start with 't'
    assert topics[0].name.startswith("t")
