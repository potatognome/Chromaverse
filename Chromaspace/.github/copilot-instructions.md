# Copilot Instructions - Chromaspace

## Purpose
Chromaspace is the core colour-geometry and registry layer for the wider Chroma ecosystem. Preserve stable interfaces, deterministic ordering, and explicit metadata.
This file is minimal by design. All general rules, agent edit policies, and centralized log/config options are defined in the modular copilot-instructions files.

Refer to:
- [Modular copilot-instructions](./copilot-instructions.d/*.md) for extensions to the general rules in this file.

## Shared Policies Propagated from dev_local/.github
- Treat this repository as its own root. Do not depend on parent dev_local paths existing on another machine.
- Keep all config, logs, tests, and output locations config-driven. Respect ROOT_MODES, PATHS, LOG_FILES, and any `.d` override directories.
- Never hardcode machine-specific absolute paths.
- Use tUilKit config and logging patterns for production code; prefer factory-based access to shared services where available.
- Use semantic colour/log keys such as `!info`, `!proc`, `!done`, `!warn`, `!error`, `!path`, `!file`, `!data`, `!test`, `!pass`, `!fail`, and `!date`.
- Keep tests deterministic and update test bootstrap files such as `tests/test_paths.json` when path behavior changes.
- Update `README.md`, `CHANGELOG.md`, `pyproject.toml`, and config version fields together when behavior or releases change.
- Keep changelog dates in `YYYY-MM-DD` format and place substantive docs under `docs/`.

## Project-Specific Rules
- Keep the Chromacore registry as a first-class subsystem with explicit module metadata and deterministic registration order.
- Preserve stable interfaces for registry-backed module types such as schemes, animations, renderers, and colour-space adapters.
- Keep geometry, colour-space logic, and semantic colour roles auditable and typed.
- Use layered config under `config/CHROMASPACE_CONFIG.json` and related override directories rather than hardcoded runtime state.
- Tests should cover registry behavior, interface compliance, geometry primitives, and deterministic colour-space output.
## Building Exemplar Policy

The `examples/` folder must include supplementary scripts that run outside pytest and stress public APIs and menu/error paths.

Requirements:
- Exercise all public functions across normal and adversarial input scenarios.
- Deliberately stress UI/menu edge cases (empty input, out-of-range values, special characters, very long strings).
- Produce visual, interactive, colour-logged output alongside structured logs for human review.
- Keep scripts as living behavior documentation.
- Maintain an `examples/exemplar.py` mock application entry point.

`examples/exemplar.py` should:
- Load tUilKit factory imports in verbose mode where available (for example, ConfigLoader).
- Generate a standard CLI menu with project header and submenus.
- Read the project primary config file.
- Read and test-load all `ROOT_MODES`.
- Verify and display resolved paths for `LOG_FILES`, config files, and input data files.
