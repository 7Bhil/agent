# 0003 - Adapter Unique et Budget de Contexte

- **Date** : 2026-10-20
- **Statut** : Accepté
- **Décideurs** : 7Bhil

## Contexte et Problématique
L'objectif du kit est de limiter les tokens consommés par les agents. Une mesure a montré trois sources de surcoût :
1. `AGENTS.md`, `GEMINI.md` et `CLAUDE.md` contenaient le même texte (environ 9 Ko chacun). Antigravity injecte `AGENTS.md` et `GEMINI.md` à chaque tour : environ 2 600 tokens dupliqués par tour.
2. La règle du premier réflexe imposait, à chaque interaction, la relecture de `BRAIN.md` et de `.agent/memory/` puis l'écriture de `current-state.md`, y compris pour une simple question.
3. `current-state.md` grossissait sans limite et aucun test ne contrôlait la taille du contexte chargé en permanence.

## Options Envisagées
1. **Conserver des adapters complets par outil** : compatibilité maximale, coût doublé dans les outils qui lisent plusieurs fichiers.
2. **Un adapter complet (`AGENTS.md`) et des renvois courts** : `CLAUDE.md` importe `AGENTS.md` via la syntaxe `@AGENTS.md` de Claude Code ; `GEMINI.md` renvoie vers `AGENTS.md`. `.cursorrules` et `copilot-instructions.md` restent complets (outils à fichier unique).

## Décision Retenue
Option 2, complétée par :
- une règle du premier réflexe proportionnée : lecture mémoire une fois par session, écriture de `current-state.md` seulement après modification de fichiers ;
- une limite de 40 lignes pour `current-state.md` (état présent, historique dans `git log`) ;
- un test de budget dans `scripts/test-kit.sh` (`AGENTS.md` <= 10 Ko, renvois <= 600 octets, `current-state.md` <= 40 lignes).

## Conséquences et Impacts
- Environ 2 600 tokens économisés par tour sous Antigravity, et 2 à 4 appels d'outils en moins pour les tours sans modification.
- Gemini CLI utilisé seul doit être configuré pour charger `AGENTS.md` (`contextFileName`), sinon l'agent suit le renvoi et lit le fichier.
- Étape suivante : compresser `AGENTS.md` sous 4 Ko en déplaçant les explications dans `core/RULES.md`.
