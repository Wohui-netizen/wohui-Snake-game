#!/usr/bin/env python3
"""贪吃蛇 v0.1.0 — Windows desktop app.

Starts a tiny read-only web server on 127.0.0.1 and opens the game in an
Edge/Chrome "app mode" window: no address bar, its own taskbar entry, the
贪吃蛇 icon and title coming from the bundled PWA manifest.

Why a server instead of opening the file directly? Browsers refuse
localStorage on file:// pages, and localStorage is what remembers the best
score and the chosen language.

Run from source:   python main.py
Check the bundle:  python main.py --selftest
"""

from __future__ import annotations

import functools
import http.server
import os
import socket
import socketserver
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser

APP_NAME = "贪吃蛇"
APP_VERSION = "0.1.0"
WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
PAGE = "index.html"
WINDOW_SIZE = "560,880"

BROWSERS = (
    r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
    r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
    r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
    r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
    r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
)


def base_dir() -> str:
    """Directory holding the bundled files (PyInstaller unpacks to _MEIPASS)."""
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))


def page_dir() -> str:
    """Folder with index.html, the manifest and the icons."""
    here = base_dir()
    bundled = os.path.join(here, "mobile")
    if os.path.isfile(os.path.join(bundled, PAGE)):
        return bundled
    repo = os.path.abspath(os.path.join(here, "..", ".."))       # running from source
    return os.path.join(repo, "app", "mobile")


def find_browser() -> str | None:
    for pattern in BROWSERS:
        path = os.path.expandvars(pattern)
        if os.path.isfile(path):
            return path
    return None


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def start_server(directory: str, port: int) -> socketserver.TCPServer:
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args, **kwargs):                  # keep the console clean
            pass

    handler = functools.partial(QuietHandler, directory=directory)
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def selftest() -> int:
    """Serve the bundled app, fetch it back, and report — no window needed."""
    import urllib.request

    directory = page_dir()
    port = free_port()
    start_server(directory, port)
    base = f"http://127.0.0.1:{port}/"
    report: list[str] = [f"{APP_NAME} {APP_VERSION} selftest", f"page folder: {directory}"]
    failures = 0

    def check(label: str, passed: bool, detail: str = "") -> None:
        nonlocal failures
        failures += 0 if passed else 1
        report.append(("PASS " if passed else "FAIL ") + label + (f" :: {detail}" if detail else ""))

    try:
        page = urllib.request.urlopen(base + PAGE, timeout=10).read().decode("utf-8")
        check("app page is served", len(page) > 10_000, f"{len(page)} bytes")
        check("game engine is bundled", "SnakeGame" in page)
        check("five languages are wired", "SNAKE_LANGUAGES" in page)
        check("touch controls are bundled", "touchmove" in page)
        check("PWA manifest is linked", 'rel="manifest"' in page)
        check("no external resources", 'src="http' not in page and 'href="http' not in page)
    except Exception as error:                                   # noqa: BLE001
        check("app page is served", False, str(error))

    for path in ("manifest.webmanifest", "icons/icon-192.png",
                 "icons/icon-512.png", "icons/icon-maskable-512.png", "sw.js"):
        try:
            data = urllib.request.urlopen(base + path, timeout=10).read()
            check(f"{path} is bundled", len(data) > 100, f"{len(data)} bytes")
        except Exception as error:                               # noqa: BLE001
            check(f"{path} is bundled", False, str(error))

    browser = find_browser()
    check("a Chromium browser is available for the app window", bool(browser),
          browser or "Edge/Chrome not found — the default browser will be used")

    report.append("RESULT: " + ("OK" if not failures else f"{failures} FAILED"))
    text = "\n".join(report)
    for target in (os.path.join(os.path.dirname(os.path.abspath(sys.executable)), "selftest.txt"),
                   os.path.join(tempfile.gettempdir(), "snake-selftest.txt")):
        try:
            with open(target, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(text + "\n")
            text += f"\nreport written to {target}"
            break
        except OSError:
            continue
    print(text)
    return 1 if failures else 0


def main(argv: list[str]) -> int:
    if "--selftest" in argv:
        return selftest()
    if "--version" in argv:
        print(f"{APP_NAME} {APP_VERSION}")
        return 0

    directory = page_dir()
    port = free_port()
    start_server(directory, port)
    url = f"http://127.0.0.1:{port}/{PAGE}"

    browser = find_browser()
    if browser:
        profile = os.path.join(tempfile.gettempdir(), "snake-app-profile")
        process = subprocess.Popen([                             # noqa: S603
            browser,
            f"--app={url}",
            f"--window-size={WINDOW_SIZE}",
            f"--user-data-dir={profile}",
            "--no-first-run",
            "--no-default-browser-check",
        ])
        try:
            process.wait()                                       # exits when the window is closed
        except KeyboardInterrupt:
            process.terminate()
        return 0

    webbrowser.open(url)                                         # last resort
    print(f"{APP_NAME} is running at {url} — press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
