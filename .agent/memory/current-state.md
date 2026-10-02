# État Courant de Session & Tâches Actives

Ce document enregistre l'état immédiat de la tâche en cours, les actions récemment exécutées et la prochaine étape prioritaire. Il permet une reprise de contexte instantanée sans saturer la fenêtre de contexte.

---

## 1. Tâche Actuelle
- **Objectif** : Refonte intégrale en **Agent Engineering OS** : Core universel, presets isolés, mémoire modulaire, installateur sécurisé, génération déterministe d'adapters et banc d'évaluations (sécurité OWASP, fintech, cycle de vie des tests).
- **Branche Active** : `feature/agent-os-refactor`.

---

## 2. Actions Complétées
- [x] **Core Universel** : Spécification de `core/RULES.md` (règles incompressibles d'ingénierie senior en 5 phases).
- [x] **Preset Isolé** : Découplage des préférences personnelles de l'auteur dans `presets/7bhil.md`.
- [x] **Refonte Mémoire Modulaire** :
  - `BRAIN.md` allégé et transformé en index opérationnel léger.
  - `.agent/memory/project.md` : Contexte technique, runtimes et outils.
  - `.agent/memory/user.md` : Préférences utilisateur actives.
  - `.agent/memory/constraints.md` : Contraintes architecturales et de sécurité.
  - `.agent/memory/current-state.md` : Suivi d'état de session vive.
- [x] **Architecture Decision Records (ADR)** :
  - Rédaction de l'ADR `docs/decisions/0002-decoupage-core-presets-memoire.md`.
  - Cadrage des critères de qualification (quand créer / quand ne pas créer d'ADR) dans `docs/decisions/README.md`.
- [x] **Installateur Sécurisé (`install.sh`)** :
  - Support de `--dry-run` (simulation sans écriture).
  - Détection des conflits de fichiers existants (préservation par défaut).
  - Support de `--force` avec création automatique de sauvegardes `.bak`.
- [x] **Générateur Déterministe d'Adapters** :
  - Implémentation de `scripts/build-adapters.py` pour synchroniser `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `templates/.github/copilot-instructions.md`.
  - Option de contrôle de parité stricte `--check`.
- [x] **Banc d'Évaluations Déterministe (Agent Evals)** :
  - `scripts/run-evals.py` : Moteur de test automatisé exécutant 4 suites de scénarios.
  - `tests/evals/agent-scenarios.md` : Scénarios généraux pass/fail.
  - `tests/evals/security-scenarios.md` : Scénarios OWASP (SQLi, secrets JWT, BOLA/IDOR, SSRF, PII).
  - `tests/evals/fintech-scenarios.md` : Scénarios fintech (anti-float, double-entry ledger, idempotence, HMAC timing-safe).
- [x] **Architecture & Design System** :
  - Spécification système dans `DESIGN.md`.
  - Découplage du guide visuel UI dans `DESIGN-SYSTEM.md`.
  - Grille opérationnelle d'exécution en 8 étapes : `checklists/08-cycle-de-travail-et-livraison.md`.
- [x] **Validation Déterministe Complète** :
  - `./scripts/test-kit.sh` exécuté au vert (parité templates, audit anti-slop, zéro émoji, dry-run/force install, ADR séquentiels, parité adapters, evals).

---

## 3. Prochaine Étape
- Validation finale de l'ensemble des contrôles en local.
- Commit sur `feature/agent-os-refactor`, merge sur `developp`, puis merge de release sur `main`.
- Push sur le dépôt distant GitHub.
