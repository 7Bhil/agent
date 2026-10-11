# État Courant de Session & Tâches Actives

Ce document enregistre l'état immédiat de la tâche en cours, les actions récemment exécutées et la prochaine étape prioritaire. Il permet une reprise de contexte instantanée sans saturer la fenêtre de contexte.

---

## 1. Tâche Actuelle
- **Objectif** : Évolution et renforcement du système Agent Engineering OS : renforcement de la règle du premier réflexe, mise à jour sélective mémoire dans l'installateur, régénération déterministe des adapters et validation des suites de tests.
- **Branche Active** : `feature/renforcement-premier-reflexe-et-install`.

---

## 2. Actions Complétées
- [x] **Renforcement de la Règle du Premier Réflexe (`core/RULES.md`)** :
  - Élargissement explicite du périmètre : application dès le premier tour et à chaque interaction (code, requêtes SQL, audit ou réponse textuelle).
  - Obligation de consulter `BRAIN.md` et `.agent/memory/`, et de mettre à jour `.agent/memory/current-state.md` avant toute réponse textuelle.
- [x] **Évolution de l'Installateur (`install.sh`)** :
  - Prise en charge du déploiement et de la mise à jour sélective de la mémoire via `--memory-only`.
  - Préservation intégrale des fichiers propres au projet existant (`AGENTS.md`, adapters, code).
  - Maintien du support de `--dry-run`, de la détection des conflits et des sauvegardes `.bak`.
- [x] **Reconstruction Déterministe des Adapters (`scripts/build-adapters.py`)** :
  - Régénération de l'ensemble des adapters (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `templates/`).
  - Validation de parité absolue vérifiée avec `python3 scripts/build-adapters.py --check`.
- [x] **Validation Déterministe et Evals** :
  - Mise à jour et exécution complète de `./scripts/test-kit.sh` (100 % succès).
  - Exécution du banc d'évaluation `python3 scripts/run-evals.py` (4/4 scénarios validés).
  - Contrôle anti-slop et zéro émoji via `python3 scripts/audit-slop.py` (0 avertissement).

---

## 3. Prochaine Étape
- Validation finale git, commit sur `feature/renforcement-premier-reflexe-et-install`.
- Fusion propre par merge commit (`--no-ff`) sur `developp`.
- Maintien de l'interdiction de merge ou push direct sur `main`.
