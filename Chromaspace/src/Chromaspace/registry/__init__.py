"""Chromacore registry public API."""

from .decorators import (
    register_animation,
    register_colour_space,
    register_emitter,
    register_renderer,
    register_scheme,
)
from .module_types import (
    MODULE_TYPE_ANIMATION_SEQUENCE,
    MODULE_TYPE_COLOUR_SPACE,
    MODULE_TYPE_EMITTER,
    MODULE_TYPE_RENDERER,
    MODULE_TYPE_SCHEME_GENERATOR,
    MODULE_TYPE_UTILITY,
)
from .registry import REGISTRY


def register(module_type, name, version, factory, capabilities, config_schema, priority=None):
    """Register a factory through the shared registry singleton."""
    return REGISTRY.register(
        module_type=module_type,
        name=name,
        version=version,
        factory=factory,
        capabilities=capabilities,
        config_schema=config_schema,
        priority=priority,
    )


def get(module_type, name):
    """Return a registered factory by module type and name."""
    return REGISTRY.get(module_type=module_type, name=name)


def get_all(module_type):
    """Return all enabled factories for a module type."""
    return REGISTRY.get_all(module_type=module_type)


def find(module_type, capability):
    """Return all enabled factories that support a capability."""
    return REGISTRY.find(module_type=module_type, capability=capability)


def disable(module_type, name):
    """Disable a registered factory by module type and name."""
    return REGISTRY.disable(module_type=module_type, name=name)


def metadata(module_type, name):
    """Return registry metadata for a factory."""
    return REGISTRY.metadata(module_type=module_type, name=name)


def freeze():
    """Freeze the registry against further mutation."""
    return REGISTRY.freeze()


__all__ = [
    "MODULE_TYPE_SCHEME_GENERATOR",
    "MODULE_TYPE_ANIMATION_SEQUENCE",
    "MODULE_TYPE_RENDERER",
    "MODULE_TYPE_COLOUR_SPACE",
    "MODULE_TYPE_EMITTER",
    "MODULE_TYPE_UTILITY",
    "register",
    "get",
    "get_all",
    "find",
    "disable",
    "metadata",
    "freeze",
    "register_scheme",
    "register_animation",
    "register_renderer",
    "register_colour_space",
    "register_emitter",
]
