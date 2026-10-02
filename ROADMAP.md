# Feuille de Route : Senior Agent Engineering OS

Cette feuille de route structure l'évolution technique et les jalons du **Senior Agent Engineering OS**.
Elle est articulée autour de garanties concrètes, automatisables et mesurables.

---

## Les 8 Phases Techniques

### Phase 1 : Core Propre & Portable (Terminé)
- [x] Découplage strict entre invariants universels (`core/RULES.md`) et préférences personnelles (`presets/7bhil.md`).
- [x] Élimination des règles codées en dur dans les instructions universelles.
- [x] Mise en place du contrat d'ingénierie senior en 5 phases.

### Phase 2 : Installation & Déploiement Sécurisé (Terminé)
- [x] Refonte complète de `install.sh` avec options `--dry-run`, `--force` et `--no-backup`.
- [x] Préservation des fichiers existants par défaut et génération de sauvegardes `.bak`.
- [x] Support d'installation locale ou distante via `curl`.

### Phase 3 : Mémoire Structurée & Découplée (Terminé)
- [x] Réduction de `BRAIN.md` à un index d'orientation opérationnel léger.
- [x] Création de `.agent/memory/` : `project.md`, `user.md`, `constraints.md`, `current-state.md`.
- [x] Standardisation des Architecture Decision Records (`docs/decisions/`).

### Phase 4 : Adapters Multi-Agents Déterministes (Terminé)
- [x] Création de `scripts/build-adapters.py` pour générer automatiquement les instructions pour chaque assistant : `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `copilot-instructions.md`.
- [x] Validation de synchronisation continue via `python3 scripts/build-adapters.py --check`.

### Phase 5 : Moteur d'Évaluation Déterministe (Agent Evals) (Terminé)
- [x] Création de `scripts/run-evals.py` avec exécution de scénarios de test rigides.
- [x] Formalisation des critères pass/fail dans `tests/evals/agent-scenarios.md`.

### Phase 6 : Évaluations de Sécurité OWASP & Fintech (Terminé)
- [x] Création de `tests/evals/security-scenarios.md` (SQLi, secrets JWT, BOLA/IDOR, SSRF, PII).
- [x] Création de `tests/evals/fintech-scenarios.md` (unités mineures, grand livre, idempotence, HMAC).
- [x] Intégration des règles d'analyse statique Semgrep (`.semgrep.yml`).

### Phase 7 : Continuous Integration & Évaluation Continue (En cours)
- [x] Découplage de la CI interne (`.github/workflows/ci.yml`) et du template projet consommateur (`templates/.github/workflows/ci.yml`).
- [x] Exécution de `scripts/test-kit.sh` et de `scripts/run-evals.py` dans le pipeline GitHub Actions.
- [ ] Ajout d'une matrice multi-runtimes (Node 18/20/22, Python 3.10/3.11/3.12).

### Phase 8 : Boucle de Rétroaction et Auto-Correction (À venir)
- [ ] Outil interactif d'analyse post-tâche comparant les modifications de l'agent au contrat d'ingénierie.
- [ ] Calcul d'un score de conformité d'agent automatique avant commit.
