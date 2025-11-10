from module_2_design_patterns_application import Observer

def test_smoke_observer():
    obj = Observer() if callable(Observer) else None
    assert obj is None or isinstance(obj, Observer)
