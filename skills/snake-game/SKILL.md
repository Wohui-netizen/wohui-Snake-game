---
name: snake-game
description: "Builds and verifies a browser-playable Snake game delivered as one self-contained HTML page: a centred grid board, Start/Pause and Difficulty buttons, a live score and best score, a five-language interface switcher (English by default), a loss when the head hits a wall or the snake's own body, and a win when the board is filled. Use when the user asks for a snake game, 贪吃蛇, or a small arcade page they can open and play right away, or wants an existing snake page adjusted (speed, board size, difficulty levels, colours, keys, touch controls, languages). Does not handle web scraping, PDF or Anki work."
---

# Snake Game (web page)

**English** · [简体中文](SKILL.zh-CN.md) · [Français](SKILL.fr.md) · [Русский](SKILL.ru.md) · [日本語](SKILL.ja.md)

## Goal

What the user wants is a snake they can play immediately, not a project that needs an environment set up. Deliver **one self-contained `index.html`** by default: HTML, CSS and JavaScript fully inline, no external dependencies, no build step, no network requests — double-click and play.

"Done" means the user can open the page and actually play it, not that the code was written.

## Fixed spec

Unless the user explicitly asks otherwise, the delivered page must satisfy all of the following:

| Area | Requirement |
| --- | --- |
| Top | Score line `Score: N　Best: M`, updated live; the best score is written to `localStorage` when a game ends and survives a refresh |
| Middle | Game area: a square grid board (20 × 20 cells by default), light teal background + white grid lines + dark border; scales down on narrow screens |
| Below | Two buttons: `Start Game` (becomes `Pause` while running, `Resume` when paused, `Restart` after a game ends) and `Difficulty: <current>` (clicking cycles through every level) |
| Snake | Purple head with two eyes, dark red body segments, each body segment carrying a small arrow showing the direction it travels |
| Food | An orange square, placed on a random free cell and never overlapping the snake |
| Difficulty | Higher difficulty means a faster snake: Easy 220 ms, Normal 150 ms, Hard 100 ms, Insane 60 ms per cell; switching mid-game applies immediately and the hint line shows the current per-cell timing |
| Loss | Head hits a wall, or head hits the snake's own body → game over, with the overlay naming the reason and showing the final score |
| Win | The snake fills every cell → the game ends as a win, and no further food is spawned |
| Controls | Arrow keys or WASD to turn, Space to pause/resume; on touch, swipe to turn and tap to pause; 180° reversals are forbidden |
| Languages | The interface ships in **English (default)**, 简体中文, Français, Русский and 日本語, with a switcher row under the buttons. Switching re-labels everything instantly and the choice is remembered; an unknown or missing stored value falls back to English |
| Status | Idle, paused and game-over states all show an overlay on the board; the status line uses `aria-live="polite"` and every button is keyboard reachable |

Turning must be buffered: pressing two direction keys in quick succession (up then left, say) must apply both, rather than dropping the second because each tick reads only one direction.

## Workflow

1. **Decide where the file goes.** Default to writing `index.html` in the current working directory; if the user gave a directory or file name, use theirs. If the target file already exists, read it first and then decide whether to overwrite, merge or save alongside — never silently discard what the user already had.
2. **Start from `assets/snake-game.html`.** Copy it to the delivery path and make incremental changes. Do not rewrite it from scratch, and do not paste it into the reply.
3. **Change only what was asked.** Keep every other baseline behaviour intact. The baseline has five change points:
   - `COLORS`: board, grid lines, border, food, body, head, arrows, eyes.
   - `DIFFICULTIES`: the level list; smaller `stepMs` means faster. The button cycles whatever levels exist, the default level comes from `difficultyIndex`, and level names live in the `difficulty` map of each language in `MESSAGES`.
   - `MESSAGES` and `LANGUAGES`: all interface wording, per language, plus the switcher row — add a sixth language by adding one `LANGUAGES` entry and one `MESSAGES` entry.
   - `new SnakeGame(canvas, { cols, rows, cell, difficultyIndex })`: board cells and cell pixel size; the canvas is resized from the cell count at runtime, so the HTML `width`/`height` attributes need no hand-editing.
   - Input layer: `KEY_DIRECTIONS` maps arrow keys and WASD; the pause key and "an arrow key starts the game when idle" live in the `keydown` handler.
   Keep the cap of at most 4 catch-up steps per frame: remove it and the snake covers dozens of cells in one go — straight into a wall — when the user returns to the tab.
4. **Self-check before delivering.** Walk the checklist below item by item, and actually look at the page in a browser when you can rather than inferring from the code that it runs. The baseline exposes `window.SnakeGame`, `window.SNAKE_DIFFICULTIES`, `window.SNAKE_LANGUAGES` and the live instance `window.snakeGame`, so you can drive and inspect a position from the browser console with `snakeGame.tick()`, `snakeGame.setDifficulty('insane')`, `snakeGame.setLanguage('ja')` or `snakeGame.render()`.
5. **Explain the hand-off.** Give the file path, how to open it (double-click, or run `python -m http.server 8000` in that directory and visit `http://localhost:8000/`), how to play, and what changed.

## Acceptance checklist

Structure and dependencies:

- One HTML file with `<script>` and `<style>` inline; no `src`, no `href`, no `fetch`, no CDN, no web fonts.
- Plays offline on double-click, with a clean browser console.

Behaviour (verify each one on the page, not just in the code):

- Pressing `Start Game` moves the snake at the current difficulty's speed.
- Pressing `Difficulty` cycles the levels; on the same board Insane is clearly faster than Easy, and a switch takes effect immediately.
- Eating the orange square adds 1 to the score, grows the snake by one segment, and respawns the food elsewhere.
- Head hits a wall → the reason is shown, the button becomes `Restart`, and a new game can be started.
- Head hits the body → same loss path; the cell the tail has just vacated must remain enterable, with no false positive.
- The snake fills every cell → judged a win, and no further food is spawned.
- Reversal keys do nothing; two legal direction keys pressed in quick succession both take effect.
- Space freezes the board and the snake stops moving; pressing it again resumes.
- Switching the language relabels the score line, both buttons, the overlay, the hint line and the page title, and the choice survives a reload; a stored value that is not a known language falls back to English.
- Leaving the tab and coming back does not make the snake cross dozens of cells and crash.
- After a refresh, `Best` still shows the previous record (degrading to "no crash" is acceptable where the browser blocks persistence).
- On a narrow screen (about 360 px wide) the board does not overflow, the buttons stay aligned, and swiping still turns the snake.

Visuals: the overall look matches the reference — score line on top, teal grid board, orange food, dark red body segments carrying arrows, purple head, and the two buttons below.

## Resources

- `assets/snake-game.html`: the complete runnable baseline game — board rendering, scoring, difficulty levels, five languages, pause, touch controls and accessibility hints. Use it as a starting point to copy, not as prose to read through.

## Boundaries

- Web scraping, PDF and Anki requests are out of scope; say so plainly when a user asks for them.
- Do not pull in frameworks, bundlers or a backend: for online multiplayer or a leaderboard, confirm with the user first and design it separately.
- Do not change the user's browser settings, and do not run installs on their behalf.
