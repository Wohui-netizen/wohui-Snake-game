# Skill Snake-game

[English](README.md) · [简体中文](README.zh-CN.md) · **Français** · [Русский](README.ru.md) · [日本語](README.ja.md)

Un Agent Skill open source qui permet à une IA de vous livrer un jeu de serpent **jouable dès l'ouverture**.

![Aperçu du jeu de serpent](docs/preview.png)

## Jouer tout de suite
**Sur n’importe quel téléphone ou ordinateur — ouvrez simplement ce lien :**

> 🎮 **https://wohui-netizen.github.io/wohui-Snake-game/skills/snake-game/assets/snake-game.html**
>
> Site de documentation (un clic change la langue sur place) : https://wohui-netizen.github.io/wohui-Snake-game/

Appuyez ensuite sur `Start Game`. Sur téléphone, balayez le plateau pour tourner, touchez pour mettre en pause, ou utilisez la croix directionnelle affichée sous les deux boutons.


Aucune installation, aucune IA, aucune compilation : le jeu est déjà dans ce dépôt, en **un seul fichier**.

1. Ouvrez **[`skills/snake-game/assets/snake-game.html`](skills/snake-game/assets/snake-game.html)** et cliquez sur **Download raw file** (ou clonez le dépôt).
2. **Double-cliquez sur le fichier téléchargé** : il s'ouvre dans votre navigateur et fonctionne hors ligne.
3. Appuyez sur **`Start Game`** (ou « Jouer » en interface française) :

| Touche / commande | Effet |
| --- | --- |
| `←` `↑` `→` `↓` ou `W` `A` `S` `D` | diriger le serpent (une flèche lance aussi la partie) |
| `Espace` | pause / reprise |
| le bouton `Difficulty: Normal` | parcourt Facile → Normal → Difficile → Enfer (plus à droite = plus rapide) |
| la ligne de langues sous les boutons | bascule l'interface entre English, 简体中文, Français, Русский, 日本語 |

Mangez les carrés orange, évitez les murs et votre propre corps, et essayez de remplir tout le plateau. Votre meilleur score est conservé.

Vous préférez une URL ? Servez le dossier puis ouvrez-le dans le navigateur :

```bash
cd skills/snake-game/assets
python -m http.server 8000
# puis ouvrez http://localhost:8000/snake-game.html
```


## 1. Quel problème cela résout-il ?

Écrire un jeu de serpent qui « fonctionne dès le double-clic » suppose de réussir simultanément une longue liste de détails délicats : la boucle temporelle et les vitesses de difficulté, trois fins différentes (toucher un mur / se mordre soi-même / remplir la grille), des touches directionnelles qui perdent les saisies trop rapides, un serpent qui se téléporte dans un mur après un aller-retour vers un autre onglet, la persistance du meilleur score, les commandes tactiles et des ressources externes qui cassent la page dès que l'on passe hors ligne. Demandez à une IA de le générer de zéro : le résultat semble jouable tout en dissimulant de vrais bugs.

Ce projet fige une **implémentation complète, validée par des tests automatisés** dans un actif de skill, et consigne la spécification de livraison ainsi qu'une liste de vérification d'acceptation dans `SKILL.md` : plutôt que d'écrire à partir de zéro, l'IA copie la base, ne modifie que ce que l'utilisateur a demandé et s'auto-contrôle point par point avant de livrer.

- **Pour les utilisateurs** : aucun environnement à installer, aucune étape de compilation — vous obtenez un seul `index.html` qui se lance au double-clic. La personnalisation ne touche qu'une poignée de points documentés et rien d'autre ne régresse.
- **Pour l'IA** : le critère du « terminé » est que l'utilisateur puisse ouvrir la page et y jouer réellement — la spécification, les conditions de fin et les vérifications sont écrites dans le skill au lieu d'être improvisées.
- **Pas pour** : le scraping web, les travaux PDF ou Anki ; ni tout ce qui exige un back-end, du multijoueur en ligne ou un classement (le skill le dit d'emblée ; cela demande une conception séparée).

## 2. Fonctionnalités principales

### 2.1 Capacités du skill

- **Spécification de livraison figée** : ligne de score en haut, grille de jeu au centre, deux boutons en dessous, apparence du serpent et de la nourriture, difficulté et vitesse, conditions de fin, commandes et messages d'état — chaque élément étant consigné dans le tableau de spécification de `SKILL.md`.
- **Flux de travail en cinq étapes** : choisir le chemin de sortie → copier `assets/snake-game.html` comme base → ne modifier que ce que l'utilisateur a nommé → exécuter la liste de vérification d'acceptation → indiquer le chemin, la façon de l'ouvrir et ce qui a changé.
- **Liste de vérification d'acceptation** : trois groupes contrôlés point par point — structure (fichier unique, aucun lien externe, console propre), comportement (manger, les trois fins, tourner, mettre en pause, meilleur score, écrans étroits) et visuel.
- **Cinq points de modification documentés** : `COLORS`, `DIFFICULTIES`, `MESSAGES` (tous les libellés de l'interface et les traductions), `new SnakeGame(canvas, { cols, rows, cell, difficultyIndex })`, et la couche de saisie (`KEY_DIRECTIONS` et le gestionnaire `keydown`).
- **Limites** : pas de scraping / PDF / Anki ; pas de frameworks, de bundlers ni de back-end.

### 2.2 Le jeu livré (mesuré sur la base)

| Domaine | Fonctionnalité |
| --- | --- |
| Forme de livraison | Un fichier HTML unique et autonome, HTML/CSS/JS entièrement en ligne, **0 référence externe**, aucune étape de compilation, jouable hors ligne au double-clic |
| Grille | 20 × 20 cellules de 24 px par défaut (480 × 480 en interne, mis à l'échelle par `devicePixelRatio` pour rester net), fond turquoise clair + lignes de grille blanches + bordure sombre, s'adapte aux fenêtres étroites |
| Score | Ligne supérieure `Score: N　Best: M`, mise à jour en direct ; le meilleur score est écrit dans `localStorage` (clé `snake-game:best-score`) à la fin d'une partie et survit à un rafraîchissement ; se dégrade sans planter lorsque le stockage est indisponible |
| Difficulté | 4 niveaux, de plus en plus rapides : Facile 220, Normal 150, Difficile 100, Enfer 60 ms par cellule, avec Normal par défaut ; un changement en cours de partie s'applique immédiatement et la ligne d'indication affiche la vitesse actuelle |
| Langues | L'interface est livrée en **anglais (par défaut)**, 简体中文, Français, Русский et 日本語. Un clic réétiquette toute la page instantanément, et le choix est mémorisé dans `localStorage` (clé `snake-game:language`) |
| Fins de partie | La tête touche un mur → défaite ; la tête touche son propre corps → défaite (la surcouche indique la raison et le score final) ; le serpent remplit toutes les cellules → victoire, et aucune autre nourriture n'apparaît |
| Virages | Jusqu'à 2 virages sont mis en mémoire tampon (les doubles appuis rapides ne sont pas perdus), les demi-tours à 180° sont refusés, et la cellule que la queue vient de libérer reste accessible |
| Commandes | Flèches / WASD pour tourner, Espace pour mettre en pause ou reprendre, une flèche démarre une partie depuis l'état initial ; au tactile, balayez pour tourner, touchez pour mettre en pause, et une croix directionnelle s'affiche sous les boutons ; un bouton ayant le focus n'avale pas l'Espace |
| Stabilité | Au plus 4 étapes de rattrapage par image : revenir sur un onglet en arrière-plan ne téléporte donc jamais le serpent dans un mur |
| Accessibilité | Ligne d'état annoncée via `role="status" aria-live="polite"`, boutons accessibles au clavier, canvas étiqueté |
| Points d'accroche de débogage | `window.snakeGame` (instance active), `window.SnakeGame` (classe), `window.SNAKE_DIFFICULTIES`, `window.SNAKE_LANGUAGES` |

## 3. Installation

**Prérequis : aucun.** Le skill lui-même est du texte brut plus un fichier HTML ; pour jouer, il suffit d'un navigateur moderne (Chrome / Edge / Firefox / Safari). Facultatif : un Python 3 quelconque, si vous souhaitez servir la page en HTTP.

### Option A : installer comme skill d'agent

1. Copiez tout le dossier du skill dans le dossier de skills de votre agent :

   ```bash
   # The exact target depends on your host; Codex-style tools read skill
   # packages from a skills directory, for example.
   cp -r skills/snake-game <your-skills-dir>/snake-game
   ```

2. Rechargez (ou redémarrez) l'hôte pour qu'il découvre le nouveau skill.
3. Invoquez-le explicitement, ou décrivez simplement ce que vous voulez et laissez le skill se déclencher :

   ```text
   $snake-game generate a snake game I can open and play right away
   ```

### Option B : aucune installation

Le fichier de base contenu dans le dossier du skill *est* le jeu complet — copiez-le, ou ouvrez-le là où il se trouve :

```bash
skills/snake-game/assets/snake-game.html
```

### Option C : l'intégrer manuellement à n'importe quelle IA

Transmettez `SKILL.md` au modèle comme instructions et `assets/snake-game.html` comme modèle de départ. Aucun hôte particulier n'est requis.

### Facultatif : vérifier que l'installation est complète

Le paquet suit l'arborescence Agent Skill ; vous pouvez donc le valider avec le script officiel skill-creator (à vous de fournir votre copie du script) :

```bash
python -X utf8 quick_validate.py skills/snake-game
# expected output: Skill is valid!
# Sous Windows avec une locale non UTF-8, ajoutez -X utf8 : le script lit SKILL.md avec l'encodage par défaut.
```

Le dossier doit contenir `SKILL.md`, `agents/openai.yaml` et `assets/snake-game.html`, sans `scripts/` superflu.

## 4. Utilisation

### 4.1 Générer ou personnaliser avec le skill

```text
$snake-game generate a snake game I can open and play right away
Adjust the snake game: 16×16 board, 3 difficulty levels, dark theme
Neon colours, bigger cells, 5 difficulty levels, press P to pause
```

Le skill ne modifie que ce que vous nommez et conserve le reste du comportement de la base ; la remise vous indique le chemin du fichier, comment l'ouvrir, comment jouer et ce qui a changé.

### 4.2 Jouer directement à la base

```bash
# Option 1: double-click it — no environment needed
skills/snake-game/assets/snake-game.html

# Option 2: serve it over HTTP
cd skills/snake-game/assets
python -m http.server 8000
# then open http://localhost:8000/snake-game.html
```

Comment jouer : cliquez sur `Jouer`, dirigez le serpent avec les **flèches / WASD**, appuyez sur **Espace** pour mettre en pause ou reprendre, et cliquez sur `Difficulté : Normal` pour parcourir les niveaux (vous pouvez changer à tout moment, y compris en cours de partie). Utilisez la rangée de langues sous les boutons pour basculer l'interface entre l'anglais, 简体中文, Français, Русский et 日本語 — la page démarre en anglais et mémorise votre choix.

### 4.3 Quoi modifier, et où

| Ce que vous voulez modifier | Où le modifier |
| --- | --- |
| Taille de la grille et taille en pixels des cellules | `new SnakeGame(canvas, { cols, rows, cell, difficultyIndex })` — le canvas est redimensionné à l'exécution d'après le nombre de cellules, les attributs HTML `width`/`height` n'ont donc pas à être modifiés à la main |
| Niveaux de difficulté, vitesses et leurs noms | `DIFFICULTIES` (identifiants et `stepMs` ; plus petit signifie plus rapide) ainsi que la table `difficulty` de chaque langue dans `MESSAGES` — le bouton parcourt tous les niveaux existants, et un nom manquant se rabat sur l'identifiant du niveau |
| Couleurs | `COLORS` (grille, lignes de grille, bordure, nourriture, corps, tête, flèches, yeux) |
| Libellés de l'interface, ou ajout d'une sixième langue | `MESSAGES` pour le texte et `LANGUAGES` pour la rangée de sélection |
| Correspondance des touches de direction et touche de pause | `KEY_DIRECTIONS` et le gestionnaire `keydown` |

### 4.4 Déboguer dans la console du navigateur

```js
snakeGame.setDifficulty('insane'); // jump to the fastest level (index also accepted)
snakeGame.setLanguage('ja');       // switch the UI language
snakeGame.tick();                  // advance one step by hand
snakeGame.snapshot();              // state, score, snake coordinates, speed, language
snakeGame.render();                // repaint the current position
snakeGame.start();                 // start a fresh game
```

## 5. Exemples d'entrée / sortie

| # | Saisie de l'utilisateur | Sortie du skill |
| --- | --- | --- |
| 1 | « Fais-moi un jeu de serpent que je peux ouvrir et auquel je peux jouer » | Copie la base vers `index.html` sans toucher à la spécification, avec la façon de l'ouvrir et d'y jouer |
| 2 | « Grille 16×16, 3 niveaux de difficulté, thème sombre » (fonctionne dans n'importe quelle langue) | La même page avec 16 lignes × 16 colonnes, 3 vitesses (200 / 120 / 70 ms), un fond sombre et un serpent émeraude ; tout le reste inchangé |
| 3 | « Couleurs néon, cellules plus grandes, 5 niveaux de difficulté, P pour la pause » | Une grille 12×12 à grandes cellules, 5 niveaux de difficulté, une palette néon, P comme touche de pause (Espace fonctionne toujours) et le texte d'indication mis à jour en conséquence |
| 4 | « Transforme le contrôle de difficulté en menu déroulant et ajoute un bouton pour rejouer » | Le contrôle de difficulté et les boutons sont remplacés sur la base ; le reste de la spécification demeure tel quel |
| 5 | « Scrape une page web pour moi / produis un PDF / crée un paquet Anki » | Explique que cela sort du périmètre du skill et ne produit pas de page de jeu |

Un résultat typique pour une demande de type 1 :

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

Les demandes de type 2 et 3 ne touchent que les points de modification listés dans « Quoi modifier, et où », après quoi la liste de vérification d'acceptation est parcourue à nouveau.

## Arborescence du dépôt

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

Il n'y a pas de `scripts/` dans le dossier du skill : cette tâche n'en a pas besoin, et le HTML de base est lui-même le modèle que vous copiez.

## Vérification

- `SKILL.md` et `agents/openai.yaml` passent le `quick_validate.py` officiel de skill-creator (sortie : `Skill is valid!`) ainsi qu'un contrôle structurel plus strict : budgets de lignes et de caractères du fichier principal, existence des chemins référencés, champs de métadonnées et vérification des dossiers vides ne signalent aucune erreur.
- La logique du jeu a été éprouvée par 24 assertions dans un vrai moteur Chromium (Edge sans interface graphique) et 87 assertions sous Node avec un simulacre de DOM, couvrant : le déplacement et l'ingestion, la collision avec un mur, la collision avec soi-même, la victoire en remplissant la grille, la correspondance difficulté-vitesse, le refus des demi-tours, la mise en mémoire tampon des virages, la pause et la reprise, la persistance du meilleur score avec un repli sûr lorsque le stockage est indisponible, le plafond de rattrapage après une longue interruption, ainsi que le contenu et les couleurs du canvas.
- La documentation d'une seule page (`index.html`) a été vérifiée dans le même navigateur sans interface avec 22 assertions : elle démarre en anglais, un clic réaffiche toute la page sur place sans navigation, le fragment d'URL suit, et le choix est mémorisé et partagé avec le jeu.
- La couche linguistique est également couverte : l'anglais est la langue par défaut, les cinq langues affichent leurs propres libellés, le changement est instantané, le choix survit à un rechargement et une valeur stockée inconnue se rabat sur l'anglais.
- Les demandes de type 1, 2 et 3 du tableau ci-dessus ont réellement été générées et retestées de bout en bout ; les images d'aperçu sont de vrais rendus de navigateur.
- Non vérifié : le comportement de `localStorage` sous `file://` varie selon les navigateurs (le code se dégrade au lieu de lever une exception).

## Licence

Publié sous [MIT License](LICENSE) : libre d'utilisation, de modification, de distribution et d'usage commercial, tant que l'avis de copyright et de licence est conservé.

```text
Copyright (c) 2026 Snake-game Skill contributors
```

Pour y mettre votre propre nom, modifiez cette ligne dans `LICENSE`.
