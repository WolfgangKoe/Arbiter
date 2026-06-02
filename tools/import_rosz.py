#!/usr/bin/env python3
"""CLI tool: import a BattleScribe .rosz or .ros roster into Arbiter YAML format.

Usage:
    python tools/import_rosz.py my_army.rosz
    python tools/import_rosz.py my_army.rosz --faction necrons
    python tools/import_rosz.py my_army.rosz --out data/rosters/
"""

import argparse
import sys
from pathlib import Path

# Add src/ to path so gameObjects can be imported
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from gameObjects.rosz_importer import (  # noqa: E402
    import_roster,
    parse_ros_bytes,
    parse_rosz_bytes,
)

_ROSTERS_DIR = Path(__file__).parent.parent / "data" / "rosters"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Import a BattleScribe .rosz roster into Arbiter YAML format"
    )
    parser.add_argument("file", type=Path, help=".rosz or .ros file to import")
    parser.add_argument(
        "--faction",
        default=None,
        help="Override auto-detected faction_dir (e.g. necrons)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=_ROSTERS_DIR,
        help=f"Output directory (default: {_ROSTERS_DIR})",
    )
    args = parser.parse_args()

    file_path: Path = args.file
    if not file_path.exists():
        print(f"ERROR: File not found: {file_path}", file=sys.stderr)
        sys.exit(1)

    suffix = file_path.suffix.lower()
    if suffix not in (".rosz", ".ros"):
        print("ERROR: Expected a .rosz or .ros file", file=sys.stderr)
        sys.exit(1)

    data = file_path.read_bytes()
    try:
        if suffix == ".rosz":
            roster_name, root = parse_rosz_bytes(data)
        else:
            roster_name, root = parse_ros_bytes(data)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    out_path, unmatched = import_roster(
        roster_name, root, faction_dir=args.faction, output_dir=args.out
    )
    print(f"Written: {out_path}")
    if unmatched:
        print(f"WARNING — {len(unmatched)} unit(s) not matched in catalog:")
        for name in unmatched:
            print(f"  - {name}")
    else:
        print("All units matched.")


if __name__ == "__main__":
    main()
