from Chromaspace.interfaces import (
    AnimationInterface,
    ColourSpaceInterface,
    RendererInterface,
    SchemeInterface,
)


def test_scheme_interface_contract():
    class DemoScheme(SchemeInterface):
        def generate(self, *args, **kwargs):
            return []

    assert isinstance(DemoScheme(), SchemeInterface)


def test_animation_interface_contract():
    class DemoAnimation(AnimationInterface):
        def generate_frames(self, *args, **kwargs):
            return []

    assert isinstance(DemoAnimation(), AnimationInterface)


def test_renderer_interface_contract():
    class DemoRenderer(RendererInterface):
        def render(self, *args, **kwargs):
            return "ok"

    assert isinstance(DemoRenderer(), RendererInterface)


def test_colour_space_interface_contract():
    class DemoColourSpace(ColourSpaceInterface):
        def to_rgb(self, h, s, l):
            return (0, 0, 0)

    assert isinstance(DemoColourSpace(), ColourSpaceInterface)
