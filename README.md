# Snake-game Skill

**English** · [简体中文](README.zh-CN.md) · [Français](README.fr.md) · [Русский](README.ru.md) · [日本語](README.ja.md)

An open-source Agent Skill that makes an AI hand you a snake game **you can play the moment it opens**.

![Snake game preview](docs/preview.png)

## Play right now
**Any phone or any computer — just open this link:**

> 🎮 **https://wohui-netizen.github.io/wohui-Snake-game/skills/snake-game/assets/snake-game.html**
>
> Documentation site (click a language to switch in place): https://wohui-netizen.github.io/wohui-Snake-game/

Then tap `Start Game`. On a phone, swipe on the board to steer and tap to pause.


No installation, no AI, no build step: the game is already in this repository as **one single file**.

1. Open **[`skills/snake-game/assets/snake-game.html`](skills/snake-game/assets/snake-game.html)** and click **Download raw file** (or clone the repository).
2. **Double-click the file you downloaded** — it opens in your browser and plays offline.
3. Press **`Start Game`**:

| Key / control | What it does |
| --- | --- |
| `←` `↑` `→` `↓` or `W` `A` `S` `D` | steer the snake (arrow keys also start the game) |
| `Space` | pause / resume |
| the `Difficulty: Normal` button | cycle Easy → Normal → Hard → Insane (further right = faster) |
| the language row under the buttons | switch the interface between English, 简体中文, Français, Русский, 日本語 |

Eat the orange squares, avoid the walls and your own body, and try to fill the whole board. Your best score is remembered between sessions.

Prefer a URL? Serve the folder and open it in the browser:

```bash
cd skills/snake-game/assets
python -m http.server 8000
# then open http://localhost:8000/snake-game.html
```


## 1. What problem does this solve?

Writing a snake game that "just works when you double-click it" means getting a long list of fiddly details right at the same time: the timing loop and difficulty speeds, three different endings (hit a wall / hit yourself / fill the board), direction keys that lose input when tapped quickly, a snake that teleports into a wall after you switch tabs and come back, high-score persistence, touch controls, and external assets that break the page the moment you go offline. Ask an AI to generate it from scratch and the result usually looks playable while hiding real bugs.

This project freezes a **complete, automated-test-verified implementation** into a skill asset, and writes the delivery spec plus an acceptance checklist into `SKILL.md`: instead of writing from scratch, the AI copies the baseline, changes only what the user asked for, and self-checks item by item before delivering.

- **For users**: no environment to install, no build step — you get one `index.html` that plays on double-click. Customisation touches a handful of documented points and nothing else regresses.
- **For the AI**: the bar for "done" is that the user can open the page and actually play it — the spec, the end conditions and the checks are written into the skill instead of being improvised.
- **Not for**: web scraping, PDF or Anki work; and anything needing a backend, online multiplayer or a leaderboard (the skill says so up front; that needs a separate design).

## 2. Main features

### 2.1 Skill capabilities

- **Fixed delivery spec**: score line on top, grid board in the middle, two buttons below, snake/food appearance, difficulty and speed, end conditions, controls and status messages — each written into the spec table in `SKILL.md`.
- **Five-step workflow**: pick the output path → copy `assets/snake-game.html` as the baseline → change only what the user named → run the acceptance checklist → report path, how to open it, and what changed.
- **Acceptance checklist**: three groups checked item by item — structure (single file, no external links, clean console), behaviour (eating, the three endings, turning, pausing, high score, narrow screens) and visuals.
- **Five documented change points**: `COLORS`, `DIFFICULTIES`, `MESSAGES` (all UI wording and translations), `new SnakeGame(canvas, { cols, rows, cell, difficultyIndex })`, and the input layer (`KEY_DIRECTIONS` and the `keydown` handler).
- **Boundaries**: no scraping / PDF / Anki; no frameworks, bundlers or backends.

### 2.2 The delivered game (measured on the baseline)

| Area | Feature |
| --- | --- |
| Delivery form | A single self-contained HTML file, HTML/CSS/JS fully inline, **0 external references**, no build step, plays offline on double-click |
| Board | 20 × 20 cells at 24 px by default (480 × 480 internally, scaled by `devicePixelRatio` to stay crisp), light teal background + white grid lines + dark border, scales down to narrow viewports |
| Score | Top line `Score: N　Best: M`, updated live; the best score is written to `localStorage` (key `snake-game:best-score`) when a game ends and survives a refresh; degrades without crashing when storage is unavailable |
| Difficulty | 4 levels, faster as difficulty rises: Easy 220, Normal 150, Hard 100, Insane 60 ms per cell, defaulting to Normal; switching mid-game applies immediately and the hint line shows the current speed |
| Languages | The UI ships in **English (default)**, 简体中文, Français, Русский and 日本語. One click re-labels the whole page instantly, and the choice is remembered in `localStorage` (key `snake-game:language`) |
| Endings | Head hits a wall → loss; head hits its own body → loss (the overlay names the reason and the final score); snake fills every cell → win, and no further food spawns |
| Turning | Up to 2 turns are buffered (quick double-taps are not lost), 180° reversals are rejected, and the cell the tail has just vacated can be entered |
| Controls | Arrow keys / WASD to turn, Space to pause or resume, an arrow key starts a game from idle; on touch, swipe to turn and tap to pause; a focused button does not swallow Space |
| Stability | At most 4 catch-up steps per frame, so returning to a backgrounded tab never teleports the snake into a wall |
| Accessibility | Status line announced via `role="status" aria-live="polite"`, keyboard-focusable buttons, labelled canvas |
| Debug hooks | `window.snakeGame` (live instance), `window.SnakeGame` (class), `window.SNAKE_DIFFICULTIES`, `window.SNAKE_LANGUAGES` |

## 3. Installation

**Requirements: none.** The skill itself is plain text plus one HTML file; playing only needs a modern browser (Chrome / Edge / Firefox / Safari). Optional: any Python 3, if you want to serve the page over HTTP.

### Option A: install as an Agent skill

1. Copy the whole skill directory into your agent's skills directory:

   ```bash
   # The exact target depends on your host; Codex-style tools read skill
   # packages from a skills directory, for example.
   cp -r skills/snake-game <your-skills-dir>/snake-game
   ```

2. Reload (or restart) the host so it discovers the new skill.
3. Invoke it explicitly, or just describe what you want and let the skill trigger itself:

   ```text
   $snake-game generate a snake game I can open and play right away
   ```

### Option B: no installation

The baseline file inside the skill directory *is* the complete game — copy it, or open it where it is:

```bash
skills/snake-game/assets/snake-game.html
```

### Option C: wire it into any AI manually

Hand `SKILL.md` to the model as instructions and `assets/snake-game.html` as the template. No specific host required.

### Optional: check that the install is complete

The package follows the Agent Skill layout, so you can validate it with the official skill-creator script (bring your own copy of the script):

```bash
python -X utf8 quick_validate.py skills/snake-game
# expected output: Skill is valid!
# On Windows with a non-UTF-8 locale, add -X utf8: the script reads SKILL.md with the default encoding.
```

The directory should contain `SKILL.md`, `agents/openai.yaml` and `assets/snake-game.html`, with no stray `scripts/`.

## 4. Usage

### 4.1 Generate or customise with the skill

```text
$snake-game generate a snake game I can open and play right away
Adjust the snake game: 16×16 board, 3 difficulty levels, dark theme
Neon colours, bigger cells, 5 difficulty levels, press P to pause
```

The skill changes only what you name and keeps the rest of the baseline behaviour; the hand-off tells you the file path, how to open it, how to play, and what changed.

### 4.2 Play the baseline directly

```bash
# Option 1: double-click it — no environment needed
skills/snake-game/assets/snake-game.html

# Option 2: serve it over HTTP
cd skills/snake-game/assets
python -m http.server 8000
# then open http://localhost:8000/snake-game.html
```

How to play: press `Start Game`, steer with the **arrow keys / WASD**, press **Space** to pause or resume, and click `Difficulty: Normal` to cycle through the levels (you can switch at any time, including mid-game). Use the language row under the buttons to switch the interface between English, 简体中文, Français, Русский and 日本語 — the page starts in English and remembers your choice.

### 4.3 What to change, and where

| What you want to change | Where to change it |
| --- | --- |
| Board size and cell pixel size | `new SnakeGame(canvas, { cols, rows, cell, difficultyIndex })` — the canvas is resized from the cell count at runtime, so the HTML `width`/`height` attributes need no hand-editing |
| Difficulty levels, speeds and their names | `DIFFICULTIES` (ids and `stepMs`; smaller is faster) plus the `difficulty` map inside every language of `MESSAGES` — the button cycles whatever levels exist, and a missing name falls back to the level id |
| Colours | `COLORS` (board, grid lines, border, food, body, head, arrows, eyes) |
| UI wording, or adding a sixth language | `MESSAGES` for the text and `LANGUAGES` for the switcher row |
| Arrow-key mapping and the pause key | `KEY_DIRECTIONS` and the `keydown` handler |

### 4.4 Debug in the browser console

```js
snakeGame.setDifficulty('insane'); // jump to the fastest level (index also accepted)
snakeGame.setLanguage('ja');       // switch the UI language
snakeGame.tick();                  // advance one step by hand
snakeGame.snapshot();              // state, score, snake coordinates, speed, language
snakeGame.render();                // repaint the current position
snakeGame.start();                 // start a fresh game
```

## 5. Input / output examples

| # | User input | Skill output |
| --- | --- | --- |
| 1 | "Make me a snake game I can open and play" | Copies the baseline to `index.html` with the spec untouched, plus how to open it and how to play |
| 2 | "16×16 board, 3 difficulty levels, dark theme" (works in any language) | The same page with 16 rows × 16 columns, 3 speeds (200 / 120 / 70 ms), a dark background and an emerald snake; everything else unchanged |
| 3 | "Neon colours, bigger cells, 5 difficulty levels, P to pause" | A 12×12 large-cell board, 5 difficulty levels, a neon palette, P as the pause key (Space still works), and the hint text updated to match |
| 4 | "Turn the difficulty control into a dropdown and add a restart button" | The difficulty control and buttons are replaced on the baseline; the rest of the spec stays as it is |
| 5 | "Scrape a web page for me / produce a PDF / build an Anki deck" | Explains that this is outside the skill's scope and does not produce a game page |

A typical result for request type 1:

```text
index.html        # one self-contained file, double-click to play (~830 lines, 0 external dependencies)
```

```text
Created index.html (20×20 board, default difficulty "Normal").
To open: double-click it, or run python -m http.server 8000 in this directory and visit http://localhost:8000/
Controls: arrow keys / WASD to turn, Space to pause, click "Difficulty" to cycle levels (Easy 220 → Insane 60 ms per cell).
The interface ships in English by default and switches to 简体中文, Français, Русский or 日本語 from the language row.
No spec changes were made; this matches the baseline.
```

Request types 2 and 3 only touch the change points listed under "What to change, and where", after which the acceptance checklist is walked through again.

## Repository layout

```text
README.md                  # this file (English, the default)
README.zh-CN.md            # 简体中文
README.fr.md               # Français
README.ru.md               # Русский
README.ja.md               # 日本語
index.html                 # single-page documentation: click a language to re-render in place
LICENSE                    # MIT licence
skills/snake-game/
├── SKILL.md               # English: delivery spec, workflow, acceptance checklist, boundaries
├── SKILL.zh-CN.md         # 简体中文
├── SKILL.fr.md            # Français
├── SKILL.ru.md            # Русский
├── SKILL.ja.md            # 日本語
├── agents/openai.yaml     # UI metadata: display_name / short_description / default_prompt
└── assets/snake-game.html # the complete runnable baseline game (rendering, score, difficulty, languages, pause, touch, accessibility)
docs/preview.png           # preview above (English UI, real browser render)
docs/preview.zh-CN.png     # the same board with the Chinese UI
```

There is no `scripts/` inside the skill directory: this task does not need one, and the baseline HTML is itself the template you copy.

## Verification

- `SKILL.md` and `agents/openai.yaml` pass the official skill-creator `quick_validate.py` (output: `Skill is valid!`) and also a stricter structural check: main-file line and character budgets, referenced-path existence, metadata fields and empty-directory checks all report 0 errors.
- The game logic was exercised with 24 assertions in a real Chromium engine (headless Edge) and 87 assertions under Node with a DOM stub, covering: movement and eating, wall collision, self collision, winning by filling the board, the difficulty-to-speed mapping, reversal rejection, turn buffering, pause and resume, high-score persistence with a safe fallback when storage is unavailable, the catch-up cap after a long stall, and the canvas contents and colours.
- The single-page documentation in `index.html` was verified in the same headless browser with 22 assertions: it starts in English, one click re-renders the whole page in place without navigating, the URL hash follows, and the choice is stored and shared with the game.
- The language layer is covered too: the default is English, all five languages render their own labels, switching is instant, the choice survives a reload, and an unknown stored value falls back to English.
- Request types 1, 2 and 3 in the table above were actually generated and re-tested end to end; the preview images are real browser renders.
- Not verified: `localStorage` behaviour under `file://` varies between browsers (the code degrades instead of throwing).

## License

Released under the [MIT License](LICENSE): free to use, modify, distribute and use commercially, as long as the copyright and licence notice are kept.

```text
Copyright (c) 2026 Snake-game Skill contributors
```

To put your own name on it, edit that one line in `LICENSE`.
