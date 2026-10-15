#!/usr/bin/env python3
"""贪吃蛇 v0.2.0 — standalone desktop game (tkinter, 中英双语).

No browser, no network, no third-party packages: only the Python standard
library. Double-click the exe and a native window opens straight into the game.

Run from source:  python snake.py
"""

from __future__ import annotations

import json
import os
import random
import sys
import tkinter as tk

APP_NAME = "贪吃蛇"
APP_VERSION = "0.2.0"

COLS = ROWS = 20
CELL = 24
BOARD_W = COLS * CELL
BOARD_H = ROWS * CELL

BOARD_BG = "#85e8d0"
GRID_LINE = "#c9f5e8"
FOOD = "#ff9f1c"
BODY = "#b23a3a"
HEAD = "#7b4fd8"
ARROW = "#7a1f1f"
EYE = "#f6f2ff"
PAGE_BG = "#f7f8fa"
TEXT = "#1f2933"
SCORE_FG = "#a33b3b"

DIFFICULTIES = [("easy", 220), ("normal", 150), ("hard", 100), ("insane", 60)]

TEXT_TABLE = {
    "zh": {
        "title": "贪吃蛇", "score": "得分", "best": "历史最高分",
        "start": "开始游戏", "pause": "暂停游戏", "resume": "继续游戏", "restart": "重新开始",
        "difficulty": "选择难度", "lang": "English",
        "names": {"easy": "简单", "normal": "普通", "hard": "困难", "insane": "地狱"},
        "idle": "点击「开始游戏」，或用方向键立即开始",
        "paused": "已暂停 — 点「继续游戏」或按空格",
        "over": "游戏结束", "win": "恭喜通关！",
        "wall": "撞到墙壁，游戏失败", "self": "撞到自己，游戏失败",
        "filled": "全部格子已填满，恭喜通关", "final": "最终得分",
        "hint": "方向键 / WASD 转向 · 空格暂停 · 也可点下方方向键",
    },
    "en": {
        "title": "Snake", "score": "Score", "best": "Best",
        "start": "Start Game", "pause": "Pause", "resume": "Resume", "restart": "Restart",
        "difficulty": "Difficulty", "lang": "中文",
        "names": {"easy": "Easy", "normal": "Normal", "hard": "Hard", "insane": "Insane"},
        "idle": 'Click "Start Game", or press an arrow key to start',
        "paused": 'Paused — click "Resume" or press Space',
        "over": "Game Over", "win": "You Win!",
        "wall": "Hit the wall", "self": "Ran into yourself",
        "filled": "Every cell is filled", "final": "Final score",
        "hint": "Arrows / WASD to turn · Space to pause · or use the buttons below",
    },
}

DIRS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}


def store_path() -> str:
    """Where the high score and language are kept: next to the exe, else APPDATA."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(sys.executable)))
    folder = os.path.dirname(os.path.abspath(sys.executable)) if getattr(sys, "frozen", False) else base
    for candidate in (folder, os.path.join(os.environ.get("APPDATA", folder), "SnakeGame")):
        try:
            os.makedirs(candidate, exist_ok=True)
            probe = os.path.join(candidate, ".write-test")
            with open(probe, "w", encoding="utf-8") as handle:
                handle.write("ok")
            os.remove(probe)
            return os.path.join(candidate, "snake-save.json")
        except OSError:
            continue
    return os.path.join(base, "snake-save.json")


class SnakeGame:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.save_path = store_path()
        saved = self._load()
        self.lang = saved.get("lang", "zh")
        self.best = int(saved.get("best", 0))
        self.difficulty_index = 1
        self.state = "idle"          # idle | running | paused | over
        self.reason = None
        self.score = 0
        self.queued: list[tuple[int, int]] = []
        self.job = None

        root.title(f"{APP_NAME} · Snake  v{APP_VERSION}")
        root.configure(bg=PAGE_BG)
        root.resizable(False, False)

        self.score_var = tk.StringVar()
        tk.Label(root, textvariable=self.score_var, bg=PAGE_BG, fg=SCORE_FG,
                 font=("Microsoft YaHei UI", 14, "bold")).pack(pady=(14, 6))

        self.canvas = tk.Canvas(root, width=BOARD_W, height=BOARD_H, bg=BOARD_BG,
                                highlightthickness=2, highlightbackground="#0d7a70")
        self.canvas.pack()

        self.overlay = tk.Label(self.canvas, text="", bg=BOARD_BG, fg="#0b3b34",
                                font=("Microsoft YaHei UI", 13, "bold"), justify="center")
        self.overlay_window = self.canvas.create_window(
            BOARD_W // 2, BOARD_H // 2, window=self.overlay)

        row = tk.Frame(root, bg=PAGE_BG)
        row.pack(pady=12)
        self.start_btn = tk.Button(row, width=12, font=("Microsoft YaHei UI", 11),
                                   command=self.toggle_start)
        self.start_btn.pack(side="left", padx=6)
        self.diff_btn = tk.Button(row, width=16, font=("Microsoft YaHei UI", 11),
                                  command=self.next_difficulty)
        self.diff_btn.pack(side="left", padx=6)

        pad = tk.Frame(root, bg=PAGE_BG)
        pad.pack()
        layout = [("", "up", ""), ("left", "down", "right")]
        for r, line in enumerate(layout):
            for c, key in enumerate(line):
                if not key:
                    tk.Label(pad, text="", width=6, bg=PAGE_BG).grid(row=r, column=c)
                    continue
                tk.Button(pad, text={"up": "▲", "down": "▼", "left": "◀", "right": "▶"}[key],
                          width=6, font=("Segoe UI", 11),
                          command=lambda k=key: self.steer(k)).grid(row=r, column=c, padx=3, pady=3)

        bottom = tk.Frame(root, bg=PAGE_BG)
        bottom.pack(pady=(10, 4))
        self.hint = tk.Label(bottom, bg=PAGE_BG, fg="#5b6472", font=("Microsoft YaHei UI", 9))
        self.hint.pack()
        self.lang_btn = tk.Button(bottom, font=("Microsoft YaHei UI", 9), command=self.toggle_lang)
        self.lang_btn.pack(pady=(6, 14))

        root.bind("<Key>", self.on_key)
        self.reset()
        self.refresh()

    # ------------------------------------------------------------------ i18n
    def t(self, key: str) -> str:
        return TEXT_TABLE[self.lang][key]

    def level_name(self) -> str:
        return TEXT_TABLE[self.lang]["names"][DIFFICULTIES[self.difficulty_index][0]]

    def step_ms(self) -> int:
        return DIFFICULTIES[self.difficulty_index][1]

    # ----------------------------------------------------------------- state
    def _load(self) -> dict:
        try:
            with open(self.save_path, encoding="utf-8") as handle:
                return json.load(handle)
        except (OSError, ValueError):
            return {}

    def _save(self) -> None:
        try:
            with open(self.save_path, "w", encoding="utf-8") as handle:
                json.dump({"best": self.best, "lang": self.lang}, handle)
        except OSError:
            pass

    def reset(self) -> None:
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.direction = (1, 0)
        self.queued = []
        self.score = 0
        self.reason = None
        self.state = "idle"
        self.food = self.spawn_food()
        self.draw()

    def spawn_food(self):
        free = [(x, y) for y in range(ROWS) for x in range(COLS) if (x, y) not in self.snake]
        return random.choice(free) if free else None

    def start(self) -> None:
        self.reset()
        self.state = "running"
        self.refresh()
        self.schedule()

    def schedule(self) -> None:
        if self.job:
            self.root.after_cancel(self.job)
        self.job = self.root.after(self.step_ms(), self.tick)

    def toggle_start(self) -> None:
        if self.state == "running":
            self.state = "paused"
            if self.job:
                self.root.after_cancel(self.job)
                self.job = None
            self.refresh()
        elif self.state == "paused":
            self.state = "running"
            self.refresh()
            self.schedule()
        else:
            self.start()

    def next_difficulty(self) -> None:
        self.difficulty_index = (self.difficulty_index + 1) % len(DIFFICULTIES)
        self.refresh()
        if self.state == "running":
            self.schedule()

    def toggle_lang(self) -> None:
        self.lang = "en" if self.lang == "zh" else "zh"
        self._save()
        self.refresh()

    def steer(self, key: str) -> None:
        dx, dy = DIRS[key]
        if self.state in ("idle", "over"):
            self.start()
        ref = self.queued[-1] if self.queued else self.direction
        if (dx, dy) == (-ref[0], -ref[1]) or (dx, dy) == ref or len(self.queued) >= 2:
            return
        self.queued.append((dx, dy))

    def on_key(self, event) -> None:
        key = (event.keysym or "").lower()
        mapping = {"up": "up", "down": "down", "left": "left", "right": "right",
                   "w": "up", "s": "down", "a": "left", "d": "right"}
        if key in mapping:
            self.steer(mapping[key])
        elif key in ("space", " "):
            self.toggle_start()

    def tick(self) -> None:
        if self.state != "running":
            return
        if self.queued:
            nxt = self.queued.pop(0)
            if nxt != (-self.direction[0], -self.direction[1]):
                self.direction = nxt

        hx, hy = self.snake[0]
        nx, ny = hx + self.direction[0], hy + self.direction[1]
        if not (0 <= nx < COLS and 0 <= ny < ROWS):
            return self.end("wall")
        eating = self.food == (nx, ny)
        body = self.snake if eating else self.snake[:-1]
        if (nx, ny) in body:
            return self.end("self")

        self.snake.insert(0, (nx, ny))
        if eating:
            self.score += 1
            self.food = self.spawn_food()
            if self.food is None:
                return self.end("filled")
        else:
            self.snake.pop()
        self.draw()
        self.refresh_score()
        self.schedule()

    def end(self, reason: str) -> None:
        self.state = "over"
        self.reason = reason
        if self.score > self.best:
            self.best = self.score
            self._save()
        if self.job:
            self.root.after_cancel(self.job)
            self.job = None
        self.draw()
        self.refresh()

    # --------------------------------------------------------------- drawing
    def draw(self) -> None:
        c = self.canvas
        c.delete("cell")
        c.create_rectangle(0, 0, BOARD_W, BOARD_H, fill=BOARD_BG, outline="", tags="cell")
        for i in range(1, COLS):
            c.create_line(i * CELL, 0, i * CELL, BOARD_H, fill=GRID_LINE, tags="cell")
        for i in range(1, ROWS):
            c.create_line(0, i * CELL, BOARD_W, i * CELL, fill=GRID_LINE, tags="cell")
        if self.food:
            fx, fy = self.food
            c.create_rectangle(fx * CELL + 3, fy * CELL + 3,
                               (fx + 1) * CELL - 3, (fy + 1) * CELL - 3,
                               fill=FOOD, outline="", tags="cell")
        for index in range(len(self.snake) - 1, -1, -1):
            x, y = self.snake[index]
            x0, y0 = x * CELL + 2, y * CELL + 2
            c.create_rectangle(x0, y0, x0 + CELL - 4, y0 + CELL - 4,
                               fill=HEAD if index == 0 else BODY, outline="", tags="cell")
            if index > 0:
                ax, ay = self.snake[index - 1]
                if index == 0:
                    dx, dy = self.direction
                else:
                    dx, dy = (1 if ax > x else -1 if ax < x else 0), (1 if ay > y else -1 if ay < y else 0)
                mx, my = x * CELL + CELL / 2, y * CELL + CELL / 2
                size = CELL * 0.22
                c.create_polygon(mx + dx * size, my + dy * size,
                                 mx - dx * size * 0.7 - dy * size * 0.9,
                                 my - dy * size * 0.7 + dx * size * 0.9,
                                 mx - dx * size * 0.7 + dy * size * 0.9,
                                 my - dy * size * 0.7 - dx * size * 0.9,
                                 fill=ARROW, outline="", tags="cell")
        hx, hy = self.snake[0]
        dx, dy = self.direction
        bx = hx * CELL + CELL / 2 + dx * CELL * 0.18
        by = hy * CELL + CELL / 2 + dy * CELL * 0.18
        for sign in (1, -1):
            ex = bx - dy * CELL * 0.2 * sign
            ey = by + dx * CELL * 0.2 * sign
            c.create_oval(ex - 1.7, ey - 1.7, ex + 1.7, ey + 1.7,
                          fill=EYE, outline="", tags="cell")

    def refresh_score(self) -> None:
        self.score_var.set(f"{self.t('score')}: {self.score}    {self.t('best')}: {self.best}")

    def refresh(self) -> None:
        self.refresh_score()
        self.start_btn.config(text={"running": self.t("pause"), "paused": self.t("resume"),
                                    "over": self.t("restart")}.get(self.state, self.t("start")))
        self.diff_btn.config(text=f"{self.t('difficulty')}: {self.level_name()}")
        self.lang_btn.config(text=self.t("lang"))
        self.hint.config(text=self.t("hint"))
        if self.state == "idle":
            self.overlay.config(text=f"{self.t('title')}\n\n{self.t('idle')}")
            self.overlay_window and self.canvas.itemconfigure(self.overlay_window, state="normal")
        elif self.state == "paused":
            self.overlay.config(text=self.t("paused"))
            self.canvas.itemconfigure(self.overlay_window, state="normal")
        elif self.state == "over":
            head = self.t("win") if self.reason == "filled" else self.t("over")
            why = {"wall": "wall", "self": "self", "filled": "filled"}.get(self.reason, "over")
            self.overlay.config(text=f"{head}\n{self.t(why)}\n{self.t('final')}: {self.score}")
            self.canvas.itemconfigure(self.overlay_window, state="normal")
        else:
            self.canvas.itemconfigure(self.overlay_window, state="hidden")


def main() -> int:
    if "--version" in sys.argv:
        print(f"{APP_NAME} {APP_VERSION}")
        return 0
    try:                                     # opt into per-monitor scaling, best effort
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(2)      # 2 = per-monitor aware
    except Exception:                        # noqa: BLE001
        pass
    root = tk.Tk()
    root.tk.call("tk", "scaling", 1.0)       # keep our pixel maths exact
    game = SnakeGame(root)
    root.update_idletasks()
    root.update()
    game.draw()
    if "--selftest" in sys.argv:
        root.update()
        print("PASS window created")
        print("PASS canvas", BOARD_W, "x", BOARD_H)
        root.destroy()
        return 0
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
