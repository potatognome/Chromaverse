# Building Windowed Apps with the Updated Compositor

## Purpose
- Define the default architecture for terminal windowed apps built on the current tUilKit compositor primitives.
- Keep rendering, input, state, and logging separated so windowed apps stay testable and reusable.
- Ensure new windowed UI work uses the current `Canvas` / `Cursor` / `Chroma` stack instead of ad-hoc print-driven redraws.

## Canonical Compositor Stack

Treat the current terminal stack as the compositor baseline:
- `Canvas` = frame surface for whole-screen or region redraws
- `Cursor` = cursor visibility, movement, and line/screen control
- `Chroma` = ANSI colour/style application

## Rules
- Use `Canvas.draw()` for the first frame and `Canvas.redraw()` for subsequent frames.
- Keep `Cursor.hide()` / `Cursor.show()` in the render loop boundary, not scattered across business logic.
- Use `Chroma` only for presentation styling; core state should remain plain data.
- Always allow ANSI fallbacks to degrade cleanly to plain text output.

References:
- `src/tUilKit/terminal/canvas.py`
- `src/tUilKit/terminal/cursor.py`
- `src/tUilKit/terminal/chroma.py`
- `tests/terminal/test_canvas.py`
- `tests/terminal/test_cursor.py`
- `tests/terminal/test_chroma.py`

## Required Architecture

Windowed apps should be split into four layers:

1. **App state**
   - Owns domain data, selection state, focus state, and window visibility.
   - Contains no ANSI escape handling.

2. **Window/view models**
   - Each window builds a plain intermediate representation of its content.
   - Prefer returning lines/rows/sections, not printing directly.

3. **Compositor**
   - Merges window outputs into one ordered frame.
   - Owns clipping, stacking order, focus highlighting, and final line assembly.

4. **Renderer/input shell**
   - Emits the frame through `Canvas`.
   - Handles keystrokes and maps them to state changes.

Do not collapse all four responsibilities into one loop with inline `print()` calls.

## Window Construction Rules

- Build windows as independently testable units with clear inputs and outputs.
- Give each window a single responsibility: navigation, detail pane, status bar, modal, help overlay, etc.
- Keep window titles, dimensions, visible sections, and refresh behavior config-driven where practical.
- Prefer deterministic layout rules over terminal-position magic spread across multiple modules.
- Use overlays/modals as temporary composited layers, not special-case full-screen rewrites.

## Rendering Rules

- Compose a full frame before writing to stdout.
- Redraw from a single compositor boundary; avoid multiple modules writing partial frames directly.
- If only one region changes, still keep update ownership centralized in the compositor layer.
- Treat plain-text rendering as the source of truth for tests; ANSI styling is an optional presentation layer.
- When ANSI is unavailable, preserve readable ordering and labels rather than forcing cursor tricks.

## Input and Focus Rules

- Read input in one place and convert keys into semantic actions.
- Track focused window explicitly.
- Keep navigation rules local to the active window, but let the compositor own focus decoration.
- Reserve low-level cursor movement for rendering only; do not use it as application state.
- Follow `.github/copilot-instructions.d/cli_menu_patterns.md` for interactive picker behavior and redraw expectations.

## tUilKit Integration Rules

- Continue using tUilKit factories for shared services: `get_logger()`, `get_config_loader()`, `get_file_system()`, `get_colour_manager()`.
- Do not bypass the logging policy because an app is windowed; route operational events through the logger and configured `LOG_FILES`.
- Keep paths, logs, and runtime options config-driven.
- Do not add app-specific window manager behavior to tUilKit core unless it is genuinely reusable across consuming projects.

## Testing and Example Expectations

- Unit-test compositor output as plain lines first.
- Cover first draw, redraw, focus changes, empty windows, oversized content, ANSI-disabled fallback, and modal/overlay cases.
- Keep example scripts in `examples/` as living behavior documentation for interactive flows.
- Prefer tests that validate frame composition deterministically instead of snapshotting terminal noise.

## Avoid

- Ad-hoc `print()` redraw logic spread through action handlers
- Mixing business logic with ANSI escape generation
- Hardcoded machine-specific paths or terminal assumptions
- Direct class instantiation for shared tUilKit services when factories exist
- App-specific one-off compositor code in reusable core modules without a clear shared contract

## References

- `.github/copilot-instructions.d/cli_menu_patterns.md`
- `.github/copilot-instructions.d/tuilkit_enabled_apps_guidelines.md`
- `.github/copilot-instructions.d/logging_policy.md`
- `.github/copilot-instructions.d/colour_key_usage.md`

---
Last updated: 2026-05-08
