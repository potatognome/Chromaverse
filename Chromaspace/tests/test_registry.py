from Chromaspace.registry import (
    MODULE_TYPE_SCHEME_GENERATOR,
)
from Chromaspace.registry.registry import ChromacoreRegistry


def _build_registry():
    return ChromacoreRegistry()


def test_register_and_get_roundtrip():
    registry = _build_registry()

    factory = object
    registry.register(
        module_type=MODULE_TYPE_SCHEME_GENERATOR,
        name="demo",
        version="1.0.0",
        factory=factory,
        capabilities=["rotational", "circular"],
        config_schema="schemas/demo.json",
        priority=2,
    )

    assert registry.get(MODULE_TYPE_SCHEME_GENERATOR, "demo") is factory


def test_get_all_is_deterministic_by_priority_then_name():
    registry = _build_registry()

    class A:
        pass

    class B:
        pass

    class C:
        pass

    registry.register(
        module_type=MODULE_TYPE_SCHEME_GENERATOR,
        name="b",
        version="1.0.0",
        factory=B,
        capabilities=["x"],
        config_schema="schemas/b.json",
        priority=1,
    )
    registry.register(
        module_type=MODULE_TYPE_SCHEME_GENERATOR,
        name="a",
        version="1.0.0",
        factory=A,
        capabilities=["x"],
        config_schema="schemas/a.json",
        priority=1,
    )
    registry.register(
        module_type=MODULE_TYPE_SCHEME_GENERATOR,
        name="c",
        version="1.0.0",
        factory=C,
        capabilities=["x"],
        config_schema="schemas/c.json",
        priority=3,
    )

    ordered = registry.get_all(MODULE_TYPE_SCHEME_GENERATOR)
    assert ordered == [C, A, B]


def test_disable_and_freeze_behaviour():
    registry = _build_registry()

    class D:
        pass

    registry.register(
        module_type=MODULE_TYPE_SCHEME_GENERATOR,
        name="d",
        version="1.0.0",
        factory=D,
        capabilities=["x"],
        config_schema="schemas/d.json",
    )

    registry.disable(MODULE_TYPE_SCHEME_GENERATOR, "d")
    assert registry.get(MODULE_TYPE_SCHEME_GENERATOR, "d") is None

    registry.freeze()
    try:
        registry.register(
            module_type=MODULE_TYPE_SCHEME_GENERATOR,
            name="e",
            version="1.0.0",
            factory=D,
            capabilities=["x"],
            config_schema="schemas/e.json",
        )
        assert False, "register should fail after freeze"
    except RuntimeError:
        assert True
