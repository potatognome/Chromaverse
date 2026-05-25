"""Chromacore registry core implementation."""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Any, Dict, List, Optional

from .module_types import ALL_MODULE_TYPES

try:
    from tUilKit import get_logger as _get_logger

    _LOGGER = _get_logger()
except Exception:
    _LOGGER = None

_REGISTRY_LOG_FILES = [
    "logFiles/chromaspace_MASTER.log",
    "logFiles/chromaspace_SESSION.log",
]


@dataclass(frozen=True)
class RegistryRecord:
    module_type: str
    name: str
    version: str
    factory: Any
    capabilities: List[str]
    config_schema: str
    priority: int
    enabled: bool


class ChromacoreRegistry:
    """Typed module registry with deterministic lookups and metadata."""

    def __init__(self) -> None:
        self._tables: Dict[str, Dict[str, Dict[str, Any]]] = {
            module_type: {} for module_type in ALL_MODULE_TYPES
        }
        self._frozen = False
        self._lock = RLock()

    def _validate_module_type(self, module_type: str) -> None:
        if module_type not in self._tables:
            raise ValueError(f"Unsupported module_type: {module_type}")

    def _log_event(self, level: str, message: str) -> None:
        if _LOGGER is None:
            return
        try:
            if level == "error":
                _LOGGER.colour_log(
                    "!error", message, log_files=_REGISTRY_LOG_FILES
                )
            else:
                _LOGGER.colour_log(
                    "!info", message, log_files=_REGISTRY_LOG_FILES
                )
        except Exception:
            return

    def _validate_metadata(
        self,
        name: str,
        version: str,
        capabilities: List[str],
        config_schema: str,
        priority: Optional[int],
    ) -> int:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("name must be a non-empty string")
        if not isinstance(version, str) or not version.strip():
            raise ValueError("version must be a non-empty string")
        if not isinstance(capabilities, list) or not capabilities:
            raise ValueError("capabilities must be a non-empty list")
        if any(not isinstance(item, str) or not item.strip() for item in capabilities):
            raise ValueError("capabilities entries must be non-empty strings")
        if not isinstance(config_schema, str) or not config_schema.strip():
            raise ValueError("config_schema must be a non-empty string")

        if priority is None:
            return 0
        if not isinstance(priority, int):
            raise ValueError("priority must be an integer when provided")
        return priority

    def _ensure_mutable(self) -> None:
        if self._frozen:
            raise RuntimeError("Registry is frozen and cannot be modified")

    def register(
        self,
        module_type: str,
        name: str,
        version: str,
        factory: Any,
        capabilities: List[str],
        config_schema: str,
        priority: Optional[int] = None,
    ) -> Any:
        with self._lock:
            self._ensure_mutable()
            self._validate_module_type(module_type)
            validated_priority = self._validate_metadata(
                name=name,
                version=version,
                capabilities=capabilities,
                config_schema=config_schema,
                priority=priority,
            )
            table = self._tables[module_type]
            if name in table:
                raise ValueError(f"{module_type}:{name} is already registered")

            table[name] = {
                "module_type": module_type,
                "name": name,
                "version": version,
                "factory": factory,
                "capabilities": sorted(set(capabilities)),
                "config_schema": config_schema,
                "priority": validated_priority,
                "enabled": True,
            }
            self._log_event(
                "info",
                f"registry register {module_type}:{name}@{version}",
            )
            return factory

    def get(self, module_type: str, name: str) -> Optional[Any]:
        with self._lock:
            self._validate_module_type(module_type)
            record = self._tables[module_type].get(name)
            if not record or not record["enabled"]:
                return None
            return record["factory"]

    def get_all(self, module_type: str) -> List[Any]:
        with self._lock:
            self._validate_module_type(module_type)
            records = [
                value
                for value in self._tables[module_type].values()
                if value["enabled"]
            ]
            records.sort(key=lambda item: (-item["priority"], item["name"]))
            return [item["factory"] for item in records]

    def find(self, module_type: str, capability: str) -> List[Any]:
        with self._lock:
            self._validate_module_type(module_type)
            records = [
                value
                for value in self._tables[module_type].values()
                if value["enabled"] and capability in value["capabilities"]
            ]
            records.sort(key=lambda item: (-item["priority"], item["name"]))
            return [item["factory"] for item in records]

    def disable(self, module_type: str, name: str) -> None:
        with self._lock:
            self._ensure_mutable()
            self._validate_module_type(module_type)
            if name not in self._tables[module_type]:
                raise KeyError(f"{module_type}:{name} is not registered")
            self._tables[module_type][name]["enabled"] = False
            self._log_event("info", f"registry disable {module_type}:{name}")

    def metadata(self, module_type: str, name: str) -> RegistryRecord:
        with self._lock:
            self._validate_module_type(module_type)
            if name not in self._tables[module_type]:
                raise KeyError(f"{module_type}:{name} is not registered")
            data = self._tables[module_type][name]
            return RegistryRecord(
                module_type=data["module_type"],
                name=data["name"],
                version=data["version"],
                factory=data["factory"],
                capabilities=list(data["capabilities"]),
                config_schema=data["config_schema"],
                priority=data["priority"],
                enabled=data["enabled"],
            )

    def freeze(self) -> None:
        with self._lock:
            self._frozen = True
            self._log_event("info", "registry freeze")


REGISTRY = ChromacoreRegistry()
