
"""CLI script to generate the full colour_system.json."""
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from Chromaspace.generator import generate_colour_entries
from Chromaspace.export import export_to_json
from Chromaspace.cli_utils import save_json
from Chromaspace.cli_utils import (
    ensure_output_dir,
    get_output_file,
)

if __name__ == "__main__":
    colours = generate_colour_entries()
    out_path = get_output_file(
        "COLOUR_SYSTEM_JSON",
        "../output/colour_system.json",
        with_system_suffix=True,
    )
    ensure_output_dir(out_path)
    # Optionally use save_json if not using export_to_json
    # save_json(colours, out_path)
    export_to_json(colours, out_path)
    print(f"Generated {len(colours)} colours to {out_path}")
