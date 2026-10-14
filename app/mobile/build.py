#!/usr/bin/env python3
"""Build the installable mobile app (PWA) for 贪吃蛇 v0.1.0.

The game itself lives in exactly one place — the skill asset — and this script
injects the PWA wiring into a copy of it, so the two can never drift apart.

Usage:  python build.py
"""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
ASSET = REPO / "skills" / "snake-game" / "assets" / "snake-game.html"
ICONS = REPO / "app" / "icons"
TARGET = HERE / "index.html"
VERSION = "0.1.0"
APP_NAME = "贪吃蛇"

ICON_FILES = ("icon-180.png", "icon-192.png", "icon-512.png", "icon-maskable-512.png")


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not ASSET.is_file():
        fail(f"game asset not found: {ASSET}")

    html = ASSET.read_text(encoding="utf-8")
    head = (HERE / "pwa-head.html").read_text(encoding="utf-8")
    body = (HERE / "pwa-body.html").read_text(encoding="utf-8")

    for anchor in ("</head>", "</body>"):
        if html.count(anchor) != 1:
            fail(f"expected exactly one {anchor} in the asset")

    html = html.replace("</head>", head + "</head>")
    html = html.replace("</body>", body + "</body>")
    html = html.replace("<title>Snake</title>", f"<title>{APP_NAME} · Snake</title>", 1)
    TARGET.write_text(html, encoding="utf-8", newline="\n")

    # keep the icons next to the manifest, copied from the shared icon set
    out_icons = HERE / "icons"
    out_icons.mkdir(exist_ok=True)
    for name in ICON_FILES:
        source = ICONS / name
        if not source.is_file():
            fail(f"missing icon: {source}")
        shutil.copyfile(source, out_icons / name)

    manifest = json.loads((HERE / "manifest.webmanifest").read_text(encoding="utf-8"))
    if manifest["version"] != VERSION:
        fail(f"manifest version is {manifest['version']}, expected {VERSION}")

    print(f"OK   {TARGET.relative_to(REPO)}  ({TARGET.stat().st_size} bytes)")
    print(f"OK   {len(ICON_FILES)} icons copied to {out_icons.relative_to(REPO)}")
    print(f"OK   manifest {manifest['name']} v{manifest['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
