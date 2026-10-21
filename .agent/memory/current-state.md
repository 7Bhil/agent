# État Courant de Session & Tâches Actives

État présent uniquement (40 lignes maximum). L'historique est dans `git log`.

---

## 1. Tâche Actuelle
- **Objectif** : Restructuration de la racine du kit (confinement dans `.agent/`) et standard Client/Server/Admin avec dossier `shared/`.
- **Branche Active** : `feature/restructuration-racine-et-shared`.

## 2. Actions Complétées
- [x] Confinement propre sous `.agent/` de `guides/`, `checklists/` et `stacks/`. La racine est désormais épurée.
- [x] Création de `.agent/stacks/client-server-admin.md` : contrat partagé Zod, alias `@shared`, zéro URL en dur.
- [x] Mise à jour des références dans `core/RULES.md` et régénération déterministe des adapters via `build-adapters.py`.
- [x] Adaptation de `install.sh`, `scripts/test-kit.sh` et `scripts/run-evals.py` pour valider les nouveaux chemins.
- [x] Formalisation de l'ADR `docs/decisions/0005-restructuration-racine-et-client-server-admin.md`.
- [x] Banc d'intégrité `./scripts/test-kit.sh` (8/8 SUCCÈS) et banc `run-evals.py` (4/4 PASS) validés sans émoji ni slop.

## 3. Prochaine Étape
- Validation finale, commit sur `feature/restructuration-racine-et-shared` et fusion propre (`--no-ff`) sur `developp`.
