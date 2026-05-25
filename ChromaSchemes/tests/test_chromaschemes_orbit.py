from Dev.Chromaschemes.src.Chromaschemes.generators.orbit import OrbitSchemeGenerator


def test_orbit_generator_is_deterministic():
    generator = OrbitSchemeGenerator()
    first = generator.generate(10)
    second = generator.generate(10)
    assert first == second
    assert first == [10, 40, 70, 100]
