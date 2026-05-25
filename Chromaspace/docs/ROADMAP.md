# Chromaspace — Roadmap

## Priority 1 — Structural Completeness

- [ ] Move `hue.py` into `colour_spaces/` subpackage with compatibility shim
- [ ] Clean up `__init__.py` star-import chain; expose explicit public API
- [ ] Add `__version__` to `__init__.py` sourced from `pyproject.toml`

## Priority 2 — Colour Engine

- [ ] Validate OKLCh and Lab output perceptually against HSV baseline
- [ ] Add `COLOUR_METHOD` to all bundled `COLOUR_SYSTEM_CONFIG_*.json` files
- [ ] Expose `COLOUR_METHOD` toggle in CLI menu

## Priority 3 — Output & Rendering

- [ ] CSS-variable export: generate a `.css` file from the colour JSON
- [ ] Figma token export (W3C Design Tokens format)
- [ ] Dark-mode variant rendering in HTML previews
- [ ] Interactive HTML filter panel (JS-driven, embedded)

## Priority 4 — Config & Tooling

- [ ] Validate config schema on load (required keys, value ranges)
- [ ] Config editor sub-menu in CLI for tweaking bands interactively
- [ ] Watch-mode: auto-regenerate JSON when pointer or config changes

## Priority 5 — Testing & CI

- [ ] Add tests for `colour_engine` dispatch and each colour-space `to_rgb`
- [ ] Add tests for `visualization.py` output structure
- [ ] Add round-trip test: generate → export → load → verify count & names
- [ ] GitHub Actions CI on push
