# BRAIN : Index Opérationnel et Boussole de Session

Ce document est le **point d'entrée opérationnel** et l'index de mémoire du projet. Il oriente immédiatement tout agent d'IA vers les modules de référence sans saturer sa fenêtre de contexte.

---

## 1. Boussole Mémoire Rapide
Les informations sont réparties selon leur responsabilité dans `.agent/memory/` :

| Domaine | Fichier de Référence | Contenu |
| :--- | :--- | :--- |
| **Règles Universelles** | [`core/RULES.md`](core/RULES.md) | Invariants d'ingénierie senior (5 phases, OWASP, clean code). |
| **Contexte Technique** | [`.agent/memory/project.md`](.agent/memory/project.md) | Type d'application, runtimes, dépendances clés. |
| **Préférences Utilisateur** | [`.agent/memory/user.md`](.agent/memory/user.md) | Conventions d'équipe et directives actives de l'utilisateur. |
| **Contraintes Strictes** | [`.agent/memory/constraints.md`](.agent/memory/constraints.md) | Engagements de sécurité, pureté zéro dépendance. |
| **État Courant** | [`.agent/memory/current-state.md`](.agent/memory/current-state.md) | Tâche en cours, derniers accomplissements, prochaine étape. |
| **Décisions de Fond** | [`docs/decisions/`](docs/decisions/) | Architecture Decision Records (ADR numérotés). |

---

## 2. Configuration & Paramétrage Actif
- Fichier de configuration maître : [`.agent/config.yml`](.agent/config.yml).
- Preset utilisateur appliqué : [`presets/7bhil.md`](presets/7bhil.md).
- Cadre de Design System : [`DESIGN.md`](DESIGN.md).

---

## 3. Protocole Immédiat pour l'Agent
1. Consulter [`.agent/memory/current-state.md`](.agent/memory/current-state.md) pour identifier la tâche en cours.
2. Appliquer les 5 phases du Core ([`core/RULES.md`](core/RULES.md)).
3. En fin d'intervention, mettre à jour uniquement [`.agent/memory/current-state.md`](.agent/memory/current-state.md) et, si un arbitrage majeur est intervenu, consigner un ADR dans `docs/decisions/`.
