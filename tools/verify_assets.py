#!/usr/bin/env python3
"""Check asset placement, generated junk, archives, and duplicate content."""

from __future__ import annotations

import hashlib
import re
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
IMAGE_EXTENSIONS = {".avif", ".gif", ".heic", ".jpeg", ".jpg", ".png", ".svg", ".tif", ".tiff", ".webp"}
ALLOWED_EXTENSIONS = {
    "animations": IMAGE_EXTENSIONS,
    "audio": {".aac", ".aif", ".aiff", ".m4a", ".mp3", ".wav"},
    "diagrams": IMAGE_EXTENSIONS | {".pdf"},
    "equations": IMAGE_EXTENSIONS | {".pdf"},
    "images": IMAGE_EXTENSIONS,
    "logos": IMAGE_EXTENSIONS | {".pdf"},
    "other": set(),
    "pdfs": {".pdf"},
    "plots": IMAGE_EXTENSIONS | {".pdf"},
    "screenshots": IMAGE_EXTENSIONS,
    "video": {".avi", ".m4v", ".mov", ".mp4", ".mpeg", ".mpg", ".webm"},
}
JUNK = re.compile(
    r"(?:-small(?:-|\.)|^blankMoviePosterImage-|^mt-|^st-|^posterImage-)",
    re.IGNORECASE,
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def main() -> int:
    errors: list[str] = []
    hashes: dict[str, list[Path]] = defaultdict(list)

    if not ASSETS.is_dir():
        print("ERROR: assets/ is missing")
        return 1

    for directory in sorted(path for path in ASSETS.iterdir() if path.is_dir()):
        allowed = ALLOWED_EXTENSIONS.get(directory.name)
        if allowed is None:
            errors.append(f"unknown asset category: {directory.relative_to(ROOT)}")
            continue

        for path in sorted(directory.rglob("*")):
            if not path.is_file() or path.name == ".gitkeep":
                continue
            relative = path.relative_to(ROOT)
            if path.parent != directory:
                errors.append(f"nested asset: {relative}")
            if allowed and path.suffix.lower() not in allowed:
                errors.append(f"misplaced extension: {relative}")
            if JUNK.search(path.name):
                errors.append(f"generated junk: {relative}")
            hashes[digest(path)].append(relative)

    for archive in sorted(ROOT.rglob("*.zip")):
        if ".git" not in archive.parts:
            errors.append(f"ZIP archive retained: {archive.relative_to(ROOT)}")

    for paths in hashes.values():
        if len(paths) > 1:
            errors.append("duplicate content: " + ", ".join(map(str, paths)))

    for error in errors:
        print(f"ERROR: {error}")
    print(f"Checked {sum(map(len, hashes.values()))} assets; {len(errors)} error(s).")
    return bool(errors)


if __name__ == "__main__":
    sys.exit(main())
