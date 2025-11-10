from module_2_advanced_oop_concepts import Animal

def test_smoke_animal():
    obj = Animal() if callable(Animal) else None
    assert obj is None or isinstance(obj, Animal)
