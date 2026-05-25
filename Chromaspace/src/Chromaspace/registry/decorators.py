"""Registration decorators for Chromacore modules."""

from __future__ import annotations

from typing import Callable, List, Optional

from .module_types import (
    MODULE_TYPE_ANIMATION_SEQUENCE,
    MODULE_TYPE_COLOUR_SPACE,
    MODULE_TYPE_EMITTER,
    MODULE_TYPE_RENDERER,
    MODULE_TYPE_SCHEME_GENERATOR,
)
from .registry import REGISTRY


def _build_metadata(
    module_type: str,
    name: str,
    version: str,
    capabilities: List[str],
    config_schema: str,
    priority: Optional[int],
) -> dict:
    return {
        "module_type": module_type,
        "name": name,
        "version": version,
        "capabilities": list(capabilities),
        "config_schema": config_schema,
        "priority": 0 if priority is None else priority,
    }


def _register_decorator(module_type: str) -> Callable:
    def decorator_factory(
        *,
        name: str,
        version: str,
        capabilities: List[str],
        config_schema: str,
        priority: Optional[int] = None,
    ) -> Callable:
        def decorator(target):
            REGISTRY.register(
                module_type=module_type,
                name=name,
                version=version,
                factory=target,
                capabilities=capabilities,
                config_schema=config_schema,
                priority=priority,
            )
            target.__chromacore_metadata__ = _build_metadata(
                module_type=module_type,
                name=name,
                version=version,
                capabilities=capabilities,
                config_schema=config_schema,
                priority=priority,
            )
            return target

        return decorator

    return decorator_factory


register_scheme = _register_decorator(MODULE_TYPE_SCHEME_GENERATOR)
register_animation = _register_decorator(MODULE_TYPE_ANIMATION_SEQUENCE)
register_renderer = _register_decorator(MODULE_TYPE_RENDERER)
register_colour_space = _register_decorator(MODULE_TYPE_COLOUR_SPACE)
register_emitter = _register_decorator(MODULE_TYPE_EMITTER)
