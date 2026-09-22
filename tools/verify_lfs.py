#!/usr/bin/env python3
"""Check that repository binaries are covered by Git LFS attributes."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BINARY_EXTENSIONS = {
    ".aac", ".aif", ".aiff", ".avi", ".avif", ".gif", ".heic", ".jpeg",
    ".jpg", ".key", ".m4a", ".m4v", ".mov", ".mp3", ".mp4", ".mpeg",
    ".mpg", ".odp", ".pdf", ".png", ".ppt", ".pptx", ".svg", ".tif", ".tiff",
    ".wav", ".webm", ".webp",
}


def main() -> int:
    files = sorted(
        path.relative_to(ROOT)
        for directory in (ROOT / "assets", ROOT / "slides")
        for path in directory.rglob("*")
        if path.is_file() and path.suffix.lower() in BINARY_EXTENSIONS
    )
    if not files:
        print("Checked 0 binaries; 0 error(s).")
        return 0

    result = subprocess.run(
        ["git", "check-attr", "filter", "--stdin"],
        cwd=ROOT,
        input="".join(f"{path}\n" for path in files),
        capture_output=True,
        text=True,
        check=True,
    )
    filters = {
        line.rsplit(": filter: ", 1)[0]: line.rsplit(": filter: ", 1)[1]
        for line in result.stdout.splitlines()
    }
    errors = [path for path in files if filters.get(str(path)) != "lfs"]

    for path in errors:
        print(f"ERROR: not covered by Git LFS: {path}")
    print(f"Checked {len(files)} binaries; {len(errors)} error(s).")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
