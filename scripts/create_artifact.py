"""Create a small deterministic artifact describing a fixture build."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Final

DEFAULT_OUTPUT: Final = Path("build/artifacts/summary.json")


def non_empty(value: str) -> str:
    """Validate command-line metadata before it reaches the artifact boundary."""
    normalized = value.strip()
    if not normalized:
        raise argparse.ArgumentTypeError("value must not be empty")
    return normalized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the JSON artifact published by the TeamCity fixture."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"output path (default: {DEFAULT_OUTPUT.as_posix()})",
    )
    parser.add_argument(
        "--build-number",
        type=non_empty,
        default="local",
        help="TeamCity build number or 'local'",
    )
    parser.add_argument(
        "--revision",
        type=non_empty,
        default="local-working-copy",
        help="Git revision or 'local-working-copy'",
    )
    return parser.parse_args()


def create_artifact(output: Path, build_number: str, revision: str) -> None:
    payload = {
        "build_number": build_number,
        "fixture": "teamcity-pipeline-fixture",
        "revision": revision,
        "schema_version": 1,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    args = parse_args()
    create_artifact(args.output, args.build_number, args.revision)
    print(f"Created artifact: {args.output}")


if __name__ == "__main__":
    main()

