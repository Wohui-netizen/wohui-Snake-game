---
name: snake-game
description: "Construit et vérifie un jeu de serpent jouable dans le navigateur, livré sous la forme d'une seule page HTML autonome : une grille de jeu centrée, des boutons Jouer/Pause et Difficulté, un score et un meilleur score en direct, un sélecteur d'interface en cinq langues (anglais par défaut), une défaite lorsque la tête touche un mur ou le corps du serpent, et une victoire lorsque la grille est remplie. À utiliser lorsque l'utilisateur demande un jeu de serpent, 贪吃蛇, ou une petite page d'arcade qu'il peut ouvrir et jouer tout de suite, ou souhaite ajuster une page de serpent existante (vitesse, taille de la grille, niveaux de difficulté, couleurs, touches, commandes tactiles, langues). Ne traite pas le scraping web, les PDF ni Anki."
---

# Jeu de serpent (page web)

[English](SKILL.md) · [简体中文](SKILL.zh-CN.md) · **Français** · [Русский](SKILL.ru.md) · [日本語](SKILL.ja.md)

## Objectif

Ce que l'utilisateur veut, c'est un serpent auquel il peut jouer immédiatement, pas un projet nécessitant l'installation d'un environnement. Livrez par défaut **un seul `index.html` autonome** : HTML, CSS et JavaScript entièrement en ligne, aucune dépendance externe, aucune étape de compilation, aucune requête réseau — double-clic et c'est parti.

« Terminé » signifie que l'utilisateur peut ouvrir la page et y jouer réellement, pas que le code a été écrit.

## Spécification figée

Sauf demande explicite du contraire, la page livrée doit satisfaire l'ensemble des points suivants :

| Domaine | Exigence |
| --- | --- |
| Haut | Ligne de score `Score: N　Best: M`, mise à jour en direct ; le meilleur score est écrit dans `localStorage` à la fin d'une partie et survit à un rafraîchissement |
| Milieu | Zone de jeu : une grille carrée (20 × 20 cellules par défaut), fond turquoise clair + lignes de grille blanches + bordure sombre ; s'adapte aux écrans étroits |
| Bas | Deux boutons : `Jouer` (devient `Pause` en cours de partie, `Reprendre` en pause, `Rejouer` après la fin d'une partie) et `Difficulté : <actuelle>` (un clic parcourt tous les niveaux) |
| Serpent | Tête violette avec deux yeux, segments de corps rouge foncé, chaque segment portant une petite flèche indiquant la direction qu'il suit |
| Nourriture | Un carré orange, placé sur une cellule libre aléatoire et jamais superposé au serpent |
| Difficulté | Plus la difficulté est élevée, plus le serpent est rapide : Facile 220 ms, Normal 150 ms, Difficile 100 ms, Enfer 60 ms par cellule ; un changement en cours de partie s'applique immédiatement et la ligne d'indication affiche le temps par cellule actuel |
| Défaite | La tête touche un mur, ou la tête touche le corps du serpent → partie terminée, la surcouche indiquant la raison et le score final |
| Victoire | Le serpent remplit toutes les cellules → la partie se termine par une victoire, et aucune autre nourriture n'apparaît |
| Commandes | Flèches ou WASD pour tourner, Espace pour mettre en pause/reprendre ; au tactile, balayez pour tourner, touchez pour mettre en pause et utilisez la croix directionnelle affichée ; les demi-tours à 180° sont interdits |
| Langues | L'interface est livrée en **anglais (par défaut)**, 简体中文, Français, Русский et 日本語, avec une rangée de sélection sous les boutons. Le changement réétiquette tout instantanément et le choix est mémorisé ; une valeur stockée inconnue ou absente se rabat sur l'anglais |
| État | Les états initial, en pause et terminé affichent tous une surcouche sur la grille ; la ligne d'état utilise `aria-live="polite"` et tous les boutons sont accessibles au clavier |

Les virages doivent être mis en mémoire tampon : appuyer sur deux touches de direction coup sur coup (haut puis gauche, par exemple) doit appliquer les deux, au lieu de perdre la seconde parce que chaque tick ne lit qu'une seule direction.

## Flux de travail

1. **Décider où va le fichier.** Écrivez par défaut `index.html` dans le répertoire de travail courant ; si l'utilisateur a donné un répertoire ou un nom de fichier, utilisez les siens. Si le fichier cible existe déjà, lisez-le d'abord puis décidez s'il faut l'écraser, le fusionner ou enregistrer à côté — ne supprimez jamais en silence ce que l'utilisateur possédait déjà.
2. **Partir de `assets/snake-game.html`.** Copiez-le vers le chemin de livraison et procédez par modifications incrémentales. Ne le réécrivez pas de zéro et ne le collez pas dans la réponse.
3. **Ne changer que ce qui a été demandé.** Préservez tous les autres comportements de la base. La base comporte cinq points de modification :
   - `COLORS` : grille, lignes de grille, bordure, nourriture, corps, tête, flèches, yeux.
   - `DIFFICULTIES` : la liste des niveaux ; un `stepMs` plus petit signifie plus rapide. Le bouton parcourt tous les niveaux existants, le niveau par défaut vient de `difficultyIndex`, et les noms de niveaux résident dans la table `difficulty` de chaque langue dans `MESSAGES`.
   - `MESSAGES` et `LANGUAGES` : tous les libellés de l'interface, par langue, plus la rangée de sélection — ajoutez une sixième langue en ajoutant une entrée `LANGUAGES` et une entrée `MESSAGES`.
   - `new SnakeGame(canvas, { cols, rows, cell, difficultyIndex })` : les cellules de la grille et la taille en pixels des cellules ; le canvas est redimensionné à l'exécution d'après le nombre de cellules, les attributs HTML `width`/`height` n'ont donc pas à être modifiés à la main.
   - Couche de saisie : `KEY_DIRECTIONS` associe les flèches et WASD ; la touche de pause et la règle « une flèche démarre la partie à l'état initial » se trouvent dans le gestionnaire `keydown`.
   Conservez le plafond d'au plus 4 étapes de rattrapage par image : supprimez-le et le serpent traverse des dizaines de cellules d'un coup — droit dans un mur — lorsque l'utilisateur revient sur l'onglet.
4. **S'auto-contrôler avant de livrer.** Parcourez la liste ci-dessous point par point, et regardez réellement la page dans un navigateur quand vous le pouvez, au lieu de déduire du code qu'elle fonctionne. La base expose `window.SnakeGame`, `window.SNAKE_DIFFICULTIES`, `window.SNAKE_LANGUAGES` et l'instance active `window.snakeGame` : vous pouvez donc piloter et inspecter une position depuis la console du navigateur avec `snakeGame.tick()`, `snakeGame.setDifficulty('insane')`, `snakeGame.setLanguage('ja')` ou `snakeGame.render()`.
5. **Expliquer la remise.** Indiquez le chemin du fichier, la façon de l'ouvrir (double-clic, ou exécutez `python -m http.server 8000` dans ce répertoire et visitez `http://localhost:8000/`), comment jouer et ce qui a changé.

## Liste de vérification d'acceptation

Structure et dépendances :

- Un seul fichier HTML avec `<script>` et `<style>` en ligne ; aucun `src`, aucun `href`, aucun `fetch`, aucun CDN, aucune police web.
- Jouable hors ligne au double-clic, avec une console de navigateur propre.

Comportement (vérifiez chaque point sur la page, pas seulement dans le code) :

- Cliquer sur `Jouer` déplace le serpent à la vitesse de la difficulté actuelle.
- Cliquer sur `Difficulté` parcourt les niveaux ; sur la même grille, Enfer est nettement plus rapide que Facile, et un changement prend effet immédiatement.
- Manger le carré orange ajoute 1 au score, fait grandir le serpent d'un segment et fait réapparaître la nourriture ailleurs.
- La tête touche un mur → la raison est affichée, le bouton devient `Rejouer` et une nouvelle partie peut être lancée.
- La tête touche le corps → même chemin de défaite ; la cellule que la queue vient de libérer doit rester accessible, sans faux positif.
- Le serpent remplit toutes les cellules → victoire prononcée, et aucune autre nourriture n'apparaît.
- Les touches de demi-tour ne font rien ; deux touches de direction légales pressées coup sur coup prennent toutes deux effet.
- Espace fige la grille et le serpent s'arrête ; un nouvel appui reprend la partie.
- Changer la langue réétiquette la ligne de score, les deux boutons, la surcouche, la ligne d'indication et le titre de la page, et le choix survit à un rechargement ; une valeur stockée qui n'est pas une langue connue se rabat sur l'anglais.
- Quitter l'onglet et y revenir ne fait pas traverser des dizaines de cellules au serpent ni ne le fait planter.
- Après un rafraîchissement, `Best` affiche toujours le record précédent (se dégrader en « aucun plantage » est acceptable lorsque le navigateur bloque la persistance).
- Sur un écran étroit (environ 360 px de large), la grille ne déborde pas, les boutons et la croix directionnelle restent alignés, et le balayage comme la croix font tourner le serpent.

Visuel : l'aspect général correspond à la référence — ligne de score en haut, grille turquoise, nourriture orange, segments de corps rouge foncé portant des flèches, tête violette et les deux boutons en dessous.

## Ressources

- `assets/snake-game.html` : le jeu de base complet et exécutable — rendu de la grille, score, niveaux de difficulté, cinq langues, pause, commandes tactiles et indications d'accessibilité. Utilisez-le comme point de départ à copier, non comme un texte à lire d'un bout en bout.

## Limites

- Les demandes de scraping web, de PDF et d'Anki sortent du périmètre ; dites-le clairement lorsqu'un utilisateur en formule une.
- N'introduisez ni frameworks, ni bundlers, ni back-end : pour du multijoueur en ligne ou un classement, confirmez d'abord avec l'utilisateur et concevez-le séparément.
- Ne modifiez pas les réglages du navigateur de l'utilisateur et n'effectuez aucune installation en son nom.
