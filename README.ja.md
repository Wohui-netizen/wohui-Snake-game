# Snake-game Skill

[English](README.md) · [简体中文](README.zh-CN.md) · [Français](README.fr.md) · [Русский](README.ru.md) · **日本語**

オープンソースの Agent Skill です。AI が**開いた瞬間に遊べる**スネークゲームを渡してくれるようにします。

![スネークゲームのプレビュー](docs/preview.png)

## すぐに遊ぶ
**スマートフォンでもパソコンでも、このリンクを開くだけ：**

> 🎮 **https://wohui-netizen.github.io/wohui-Snake-game/skills/snake-game/assets/snake-game.html**
>
> ドキュメントサイト（クリックでその場で言語切替）：https://wohui-netizen.github.io/wohui-Snake-game/

開いたら `Start Game` を押します。スマートフォンでは盤面をスワイプして方向転換、タップで一時停止します。


インストールも AI もビルドも不要です。ゲームはこのリポジトリに**1 つのファイル**としてすでに入っています。

1. **[`skills/snake-game/assets/snake-game.html`](skills/snake-game/assets/snake-game.html)** を開き、右上の **Download raw file** をクリックします（リポジトリを clone しても同じです）。
2. **ダウンロードしたファイルをダブルクリック**するとブラウザで開き、オフラインでも遊べます。
3. **`Start Game`**（日本語界面では「ゲーム開始」）を押します：

| キー / 操作 | 動作 |
| --- | --- |
| `←` `↑` `→` `↓` または `W` `A` `S` `D` | スネークの向き（矢印キーでそのまま開始） |
| `スペース` | 一時停止 / 再開 |
| `Difficulty: Normal` ボタン | かんたん → ふつう → むずかしい → 地獄 を順に切替（右ほど速い） |
| ボタンの下の言語行 | English / 简体中文 / Français / Русский / 日本語 を切替 |

オレンジのマスを食べ、壁と自分の体を避け、盤面を埋めるのを目指します。最高スコアは保存されます。

URL で開きたい場合はローカルサーバーを立てます：

```bash
cd skills/snake-game/assets
python -m http.server 8000
# ブラウザで http://localhost:8000/snake-game.html を開く
```


## 1. 何を解決するのか

「ダブルクリックすればそのまま動く」スネークゲームを書くには、細かくて厄介な点を同時に押さえる必要があります。タイマーループと難易度ごとの速度、3 通りの終わり方（壁に衝突／自分に衝突／盤面を埋める）、素早く連打すると入力が抜ける方向キー、タブを切り替えて戻ると蛇が壁までワープする問題、最高スコアの永続化、タッチ操作、そしてオフラインになった瞬間にページが壊れる外部アセット。AI にゼロから生成させると、遊べそうに見えるのに実際にはバグが潜んでいる、という結果になりがちです。

本プロジェクトは、**自動テストで検証済みの完全な実装**をスキル資産として固定し、交付仕様と受け入れチェックリストを `SKILL.md` に書き込みました。AI はゼロから書くのではなく、ベースラインをコピーし、ユーザーが指定した箇所だけを変更し、交付前にチェックリストで項目ごとに自己点検します。

- **利用者の方へ**: 環境構築もビルドも不要です。ダブルクリックで遊べる `index.html` が 1 つ手に入ります。カスタマイズはドキュメント化された変更点だけを触ればよく、それ以外の挙動は退行しません。
- **AI へ**:「完了」の基準は、ユーザーがページを開いて実際に遊べることです。仕様・終了条件・チェック項目はその場の判断ではなく、スキル内に書き込まれています。
- **対象外**: Web スクレイピング、PDF、Anki 関連。また、バックエンドやオンライン対戦、ランキングが必要なもの（スキルが冒頭で明示します。別途設計が必要です）。

## 2. 主な機能

### 2.1 スキルの機能

- **固定の交付仕様**: 上部のスコア行、中央のグリッド盤面、下部の 2 つのボタン、蛇と餌の見た目、難易度と速度、終了条件、操作方法、ステータスメッセージを、それぞれ `SKILL.md` の仕様表に記載しています。
- **5 ステップのワークフロー**: 出力先を決める → `assets/snake-game.html` をベースラインとしてコピーする → ユーザーが指定した箇所だけを変更する → 受け入れチェックリストを実行する → パス、開き方、変更内容を報告する。
- **受け入れチェックリスト**: 構造（単一ファイル、外部リンクなし、コンソールがクリーン）、挙動（餌を食べる、3 通りの終わり方、旋回、一時停止、最高スコア、狭い画面）、見た目の 3 グループを項目ごとに確認します。
- **ドキュメント化された 5 つの変更点**: `COLORS`、`DIFFICULTIES`、`MESSAGES`（UI の文言と翻訳すべて）、`new SnakeGame(canvas, { cols, rows, cell, difficultyIndex })`、入力レイヤー（`KEY_DIRECTIONS` と `keydown` ハンドラー）。
- **境界**: スクレイピング／PDF／Anki は行いません。フレームワーク、バンドラー、バックエンドも導入しません。

### 2.2 交付されるゲーム（ベースラインでの実測値）

| 分類 | 機能 |
| --- | --- |
| 交付形態 | 単一の自己完結型 HTML ファイル。HTML/CSS/JS はすべてインラインで、**外部参照 0 件**、ビルド手順なし、オフラインでもダブルクリックで遊べます |
| 盤面 | 既定では 20 × 20 マス、1 マス 24 px（内部は 480 × 480 で、`devicePixelRatio` により拡大縮小して鮮明さを維持）。薄い青緑の背景 + 白いグリッド線 + 濃い枠線で、狭いビューポートにも縮小して収まります |
| スコア | 上部の行は `スコア: N　最高スコア: M` でリアルタイムに更新されます。最高スコアはゲーム終了時に `localStorage`（キー `snake-game:best-score`）へ書き込まれ、リロード後も保持されます。ストレージが利用できない場合もクラッシュせずに縮退します |
| 難易度 | 4 段階で、難易度が上がるほど高速です。かんたん 220、ふつう 150、むずかしい 100、地獄 60 ミリ秒／マス。既定はふつうで、ゲーム中に切り替えると即座に反映され、ヒント行に現在の速度が表示されます |
| 言語 | UI は**英語（既定）**、简体中文、Français、Русский、日本語に対応しています。ワンクリックでページ全体のラベルが即座に切り替わり、選択は `localStorage`（キー `snake-game:language`）に記憶されます |
| 終了条件 | 頭が壁に衝突 → 敗北。頭が自分の胴体に衝突 → 敗北（オーバーレイに理由と最終スコアを表示）。蛇がすべてのマスを埋める → 勝利で、以降は餌が出現しません |
| 旋回 | 最大 2 回の旋回をバッファリングし（素早い二度押しでも入力が抜けません）、180° の反転は拒否され、しっぽが直前まで占めていたマスには進入できます |
| 操作 | 方向キー／WASD で旋回、Space で一時停止または再開、待機中は方向キーでゲームが始まります。タッチではスワイプで旋回、タップで一時停止します。フォーカス中のボタンが Space を奪うことはありません |
| 安定性 | 1 フレームあたりの追いつき処理は最大 4 ステップなので、バックグラウンドのタブから戻っても蛇が壁までワープしません |
| アクセシビリティ | ステータス行は `role="status" aria-live="polite"` で通知され、ボタンはキーボードでフォーカス可能、キャンバスにはラベルがあります |
| デバッグフック | `window.snakeGame`（実行中のインスタンス）、`window.SnakeGame`（クラス）、`window.SNAKE_DIFFICULTIES`、`window.SNAKE_LANGUAGES` |

## 3. インストール

**必要なもの: ありません。** スキル自体はプレーンテキストと 1 つの HTML ファイルです。遊ぶにはモダンなブラウザー（Chrome / Edge / Firefox / Safari）だけが必要です。任意で、ページを HTTP で配信したい場合は任意の Python 3 をご利用ください。

### 方法 A: Agent スキルとしてインストールする

1. スキルディレクトリ全体を、お使いのエージェントのスキルディレクトリへコピーします:

   ```bash
   # The exact target depends on your host; Codex-style tools read skill
   # packages from a skills directory, for example.
   cp -r skills/snake-game <your-skills-dir>/snake-game
   ```

2. ホストを再読み込み（または再起動）して、新しいスキルを認識させます。
3. 明示的に呼び出すか、ご希望の内容をそのまま伝えてスキルを自動的に発動させます:

   ```text
   $snake-game generate a snake game I can open and play right away
   ```

### 方法 B: インストールしない

スキルディレクトリ内のベースラインファイルが、そのまま完全なゲームです。コピーするか、その場で開いてください:

```bash
skills/snake-game/assets/snake-game.html
```

### 方法 C: 任意の AI に手動で組み込む

`SKILL.md` を指示として、`assets/snake-game.html` をテンプレートとしてモデルに渡します。特定のホストは必要ありません。

### 任意: インストールが完全か確認する

このパッケージは Agent Skill のレイアウトに従っているため、公式の skill-creator スクリプトで検証できます（スクリプトはご自身でご用意ください）:

```bash
python -X utf8 quick_validate.py skills/snake-game
# expected output: Skill is valid!
# 非 UTF-8 ロケールの Windows では -X utf8 を付けてください。スクリプトは SKILL.md を既定のエンコーディングで読み込みます。
```

ディレクトリには `SKILL.md`、`agents/openai.yaml`、`assets/snake-game.html` が含まれ、余計な `scripts/` は存在しない状態にしてください。

## 4. 使い方

### 4.1 スキルで生成・カスタマイズする

```text
$snake-game generate a snake game I can open and play right away
Adjust the snake game: 16×16 board, 3 difficulty levels, dark theme
Neon colours, bigger cells, 5 difficulty levels, press P to pause
```

スキルは指定された箇所だけを変更し、ベースラインのその他の挙動は維持します。引き渡し時には、ファイルパス、開き方、遊び方、変更内容をお伝えします。

### 4.2 ベースラインをそのまま遊ぶ

```bash
# Option 1: double-click it — no environment needed
skills/snake-game/assets/snake-game.html

# Option 2: serve it over HTTP
cd skills/snake-game/assets
python -m http.server 8000
# then open http://localhost:8000/snake-game.html
```

遊び方: `ゲーム開始` を押し、**方向キー／WASD** で操作します。**Space** を押すと一時停止または再開し、`難易度: ふつう` をクリックすると段階が順に切り替わります（ゲーム中を含め、いつでも切り替えられます）。ボタンの下の言語行を使うと、インターフェースを英語、简体中文、Français、Русский、日本語の間で切り替えられます。ページは英語で起動し、選択内容を記憶します。

### 4.3 何をどこで変更するか

| 変更したい内容 | 変更箇所 |
| --- | --- |
| 盤面の大きさと 1 マスのピクセル数 | `new SnakeGame(canvas, { cols, rows, cell, difficultyIndex })` — キャンバスは実行時にマス数からサイズが決まるため、HTML の `width`/`height` 属性を手で編集する必要はありません |
| 難易度の段階、速度、その名称 | `DIFFICULTIES`（id と `stepMs`。小さいほど高速）と、`MESSAGES` の各言語内にある `difficulty` マップ — ボタンは存在する段階をすべて循環し、名称が欠けている場合は段階の id にフォールバックします |
| 配色 | `COLORS`（盤面、グリッド線、枠線、餌、胴体、頭、矢印、目） |
| UI の文言、または 6 つ目の言語の追加 | テキストは `MESSAGES`、切り替え行は `LANGUAGES` |
| 方向キーの割り当てと一時停止キー | `KEY_DIRECTIONS` と `keydown` ハンドラー |

### 4.4 ブラウザーコンソールでデバッグする

```js
snakeGame.setDifficulty('insane'); // jump to the fastest level (index also accepted)
snakeGame.setLanguage('ja');       // switch the UI language
snakeGame.tick();                  // advance one step by hand
snakeGame.snapshot();              // state, score, snake coordinates, speed, language
snakeGame.render();                // repaint the current position
snakeGame.start();                 // start a fresh game
```

## 5. 入出力の例

| # | ユーザーの入力 | スキルの出力 |
| --- | --- | --- |
| 1 | 「開いてすぐ遊べるスネークゲームを作って」 | 仕様を変えずにベースラインを `index.html` へコピーし、開き方と遊び方を添えて渡します |
| 2 | 「16×16 の盤面、難易度 3 段階、ダークテーマ」（どの言語でも可） | 同じページを 16 行 × 16 列、速度 3 段階（200 / 120 / 70 ミリ秒）、暗い背景とエメラルド色の蛇に変更します。それ以外は変更しません |
| 3 | 「ネオンカラー、マスを大きく、難易度 5 段階、P で一時停止」 | 12×12 の大きなマスの盤面、難易度 5 段階、ネオンの配色、一時停止キーを P に変更（Space も引き続き有効）し、ヒントの文言も合わせて更新します |
| 4 | 「難易度の操作をドロップダウンにして、もう一度ボタンを追加して」 | ベースライン上で難易度の操作とボタンを置き換えます。仕様のその他の部分はそのままです |
| 5 | 「Web ページをスクレイピングして／PDF を作って／Anki デッキを作って」 | スキルの範囲外であることを説明し、ゲームページは生成しません |

リクエスト 1 の典型的な結果:

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

リクエスト 2 と 3 では、「何をどこで変更するか」に挙げた変更点だけを触り、その後に受け入れチェックリストをもう一度通します。

## リポジトリ構成

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

スキルディレクトリ内に `scripts/` はありません。このタスクには不要で、ベースラインの HTML 自体がコピー元のテンプレートだからです。

## 検証

- `SKILL.md` と `agents/openai.yaml` は公式の skill-creator `quick_validate.py` に合格し（出力: `Skill is valid!`）、さらに厳格な構造チェックも通過しています。本体ファイルの行数・文字数の上限、参照パスの存在、メタデータの項目、空ディレクトリの確認はいずれもエラー 0 件です。
- ゲームロジックは、実際の Chromium エンジン（ヘッドレス Edge）で 24 件、DOM スタブを用いた Node で 87 件のアサーションにより検証しました。対象は、移動と捕食、壁への衝突、自己衝突、盤面を埋めることによる勝利、難易度と速度の対応、反転の拒否、旋回のバッファリング、一時停止と再開、ストレージが使えない場合の安全なフォールバックを伴う最高スコアの永続化、長時間の停止後の追いつき上限、キャンバスの内容と色です。
- 1 ページ版ドキュメント（`index.html`）も同じヘッドレスブラウザで 22 件のアサーションにより検証しました。既定は英語で、クリックするとページ遷移せずその場で全体が切り替わり、URL のハッシュも更新され、選択は記憶されゲームと共有されます。
- 言語レイヤーも対象です。既定は英語で、5 つの言語すべてがそれぞれのラベルを描画し、切り替えは即座に反映され、選択はリロード後も保持され、保存された未知の値は英語にフォールバックします。
- 上記の表にあるリクエスト 1、2、3 は実際に生成し、エンドツーエンドで再テストしました。プレビュー画像は実際のブラウザーでのレンダリング結果です。
- 未検証: `file://` での `localStorage` の挙動はブラウザーによって異なります（コードは例外を投げずに縮退します）。

## ライセンス

[MIT License](LICENSE) の下で公開しています。著作権表示とライセンス表示を保持していれば、使用、変更、配布、商用利用は自由です。

```text
Copyright (c) 2026 Snake-game Skill contributors
```

ご自身の名前を表示したい場合は、`LICENSE` のその 1 行を編集してください。
