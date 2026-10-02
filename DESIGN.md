# Architecture Globale du Senior Agent Engineering OS

Ce document présente l'architecture système, les flux d'exécution et les responsabilités des composants du **Senior Agent Engineering OS**.

---

## 1. Vue d'Ensemble & Découpage Système

Le système est articulé autour d'un **Core universel déterministe**, isolé des préférences subjectives et des contraintes d'environnements spécifiques.

```
                               Core Universel (core/RULES.md)
                                             |
                   +-------------------------+-------------------------+
                   |                                                   |
                   v                                                   v
   Générateur d'Adapters (scripts/build-adapters.py)       Presets Utilisateur (presets/)
                   |                                                   |
                   +-------------------------+-------------------------+
                                             |
                                             v
               Instructions Multi-Agents (AGENTS, GEMINI, CLAUDE, Cursor...)
                                             |
                                             v
                                  Agent IA en Session
                                             |
                   +-------------------------+-------------------------+
                   |                                                   |
                   v                                                   v
      Mémoire Modulaire (.agent/memory/)                     Code & Architecture Projet
      - project.md (contexte technique)                      - Implémentation typée
      - user.md (directives actives)                         - Design System (DESIGN.md)
      - constraints.md (invariants)                          - Stacks spécialisées (stacks/)
      - current-state.md (session vive)                      - Décisions structurantes (ADR)
                                             |
                                             v
                           Banc d'Évaluations & Contrôles
                           - scripts/test-kit.sh (Intégrité)
                           - scripts/run-evals.py (Scénarios IA)
                           - .semgrep.yml (Analyse Statique)
                           - scripts/audit-slop.py (Sobriété)
```

---

## 2. Matrice des Responsabilités & Rôles

Le système distingue formellement cinq niveaux d'intervention pour éviter toute ambiguïté :

| Composant | Nature | Emplacement | Fonction & Garantie |
| :--- | :--- | :--- | :--- |
| **Core Invariants** | Instruction formelle | `core/RULES.md` | Socle universel d'ingénierie senior (5 phases, OWASP, clean code). |
| **Presets** | Configuration personnelle | `presets/7bhil.md` | Conventions spécifiques (commits en français, conventions de branches). |
| **Adapters** | Fichiers dérivés | Racine & `templates/` | Points d'ancrage pour chaque assistant IA (`AGENTS.md`, `CLAUDE.md`, etc.). |
| **Mémoire Vive** | Contexte dynamique | `.agent/memory/` | Contexte technique, directives, contraintes et état de session. |
| **Décisions (ADR)** | Historique immuable | `docs/decisions/` | Enregistrements formels d'arbitrages architecturaux majeurs. |
| **Vérifications Statiques** | Automatisation déterministe | Scripts & CI | `test-kit.sh`, `run-evals.py`, Semgrep, audit anti-slop. |

---

## 3. Ce qui est Garanti par l'Outillage vs ce qui Repose sur le Prompt

Une architecture d'agent honnête et rigoureuse doit expliciter ses limites :

### Garanties Automatisées (Bloquantes en Machine)
1. **Parité des Fichiers d'Agents** : `scripts/build-adapters.py --check` empêche toute divergence entre le Core et les adapters déployés.
2. **Pureté Textuelle & Anti-Slop** : `scripts/audit-slop.py` bloque en pré-commit et en CI les tics de langage et le remplissage artificiel.
3. **Zéro Émoji dans les Fichiers d'Ingénierie** : Contrôle binaire Unicode dans `scripts/test-kit.sh`.
4. **Numérotation et Format des ADR** : Validation séquentielle stricte par script.
5. **Injections SQL & Secrets en Dur** : Règles d'analyse statique `.semgrep.yml` et scan de secrets Gitleaks.
6. **Déploiement Sécurisé Sans Écrasement** : `install.sh` garantit la détection des fichiers existants, le mode `--dry-run` et la création de sauvegardes `.bak`.

### Garanties Portées par les Instructions (Contrat d'Agent)
1. **Application Rigoureuse de la Phase 0** : Écriture spontanée de tests de caractérisation avant de refactoriser du code patrimonial sans tests.
2. **Arithmétique Financière & Grand Livre** : Modélisation des transactions financières en unités mineures et écriture en partie double (`stacks/fintech.md`).
3. **Gestion du Cycle de Vie des Tests** : Décision autonome d'ajouter des tests pour les cas limites ou de purger les tests d'une fonctionnalité dépréciée.
4. **Respect des Directives Métier** : Consultation autonome de `BRAIN.md` et mise à jour de l'état de session dans `.agent/memory/current-state.md`.

---

## 4. Flux de Travail et Boucle de Rétroaction (*Agent Feedback Loop*)

```
[Tâche Utilisateur] 
         |
         v
1. Lecture de BRAIN.md et .agent/memory/
         |
         v
2. Phase 0 : Exécution de la suite de tests existante (Ligne de base)
         |
         v
3. Investigation & Diagnostic de la cause racine
         |
         v
4. Implémentation Clean Code (Zéro any, respect DESIGN.md)
         |
         v
5. Tests Automatisés (Nominal, limites, anti-régression)
         |
         v
6. Contrôle Local : scripts/test-kit.sh & scripts/run-evals.py
         |
         +--> [ÉCHEC] : Auto-correction immédiate de l'agent
         |
         +--> [SUCCÈS] : Mise à jour de .agent/memory/current-state.md
```
