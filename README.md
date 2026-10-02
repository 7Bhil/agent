# Senior Agent Engineering OS

> Système d'exploitation d'ingénierie logicielle pour agents IA : portable, déterministe, testable et multi-assistants (Gemini/Antigravity, Claude, Cursor, GitHub Copilot, Codex, Windsurf, Cline).

---

## 1. Ce Qu'est le Projet & Le Problème Qu'il Résout

La plupart des kits pour assistants IA se résument à des collections de prompts verbeux. En pratique, ces consignes informelles échouent régulièrement en production :
- L'agent invente des bibliothèques ou des méthodes inexistantes (hallucinations).
- L'agent produit du code non typé (`any`) ou des couleurs arbitraires en ligne (`#hex`).
- L'agent applique des modifications aveugles sur du code patrimonial sans en vérifier la ligne de base.
- Les fichiers d'instructions se contredisent selon l'éditeur utilisé (Cursor vs Claude vs Copilot).

Le **Senior Agent Engineering OS** transforme cette approche : il fournit un **socle universel d'ingénierie logicielle**, une **mémoire structurée**, des **générateurs déterministes d'adapters** et un **banc d'évaluation automatisé**.

---

## 2. Architecture du Système

Le dépôt applique une séparation stricte des responsabilités :

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
      - user.md (directives actives)                         - Design System (DESIGN-SYSTEM.md)
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

## 3. Installation et Déploiement

### Déploiement en 1 Commande (Projet Existant ou Neuf)
```bash
curl -sSL https://raw.githubusercontent.com/7Bhil/agent/main/install.sh | bash
```

### Options d'Installation Avancées
Le script d'installation est sécurisé par défaut : il ne détruit jamais silencieusement votre travail.
```bash
# Simuler l'installation sans écrire sur le disque
./install.sh --dry-run

# Forcer le remplacement des fichiers existants (crée automatiquement des copies .bak)
./install.sh --force

# Remplacer sans créer de copies de sauvegarde
./install.sh --force --no-backup
```

---

## 4. Ce Qui Est Automatisé vs Ce Qui Repose sur les Prompts

Une ingénierie honnête explicite ses garanties réelles :

### Garanties Automatisées Déterministes (Bloquantes en Machine)
- **Parité d'Adapters** : `python3 scripts/build-adapters.py --check` garantit que tous les fichiers assistants dérivent du Core sans dérive textuelle.
- **Pureté Textuelle Anti-Slop** : `python3 scripts/audit-slop.py` bloque en pré-commit et CI le remplissage artificiel et les tics de langage IA.
- **Zéro Émoji Garanti** : Scan binaire Unicode dans `scripts/test-kit.sh`.
- **Analyse Statique Sécurité** : Détection des requêtes SQL concaténées et secrets JWT en dur via Semgrep (`.semgrep.yml`).
- **Ordonnancement des Décisions** : Contrôle séquentiel strict des fichiers ADR (`docs/decisions/`).

### Garanties Portées par les Instructions d'Agents
- **Phase 0 d'Onboarding** : Exécution systématique des tests de caractérisation préalables au refactoring patrimonial ([`guides/onboard-codebase.md`](guides/onboard-codebase.md)).
- **Rigueur Financière** : Manipulation monétaire exclusive en unités mineures et grand livre immuable à double entrée ([`stacks/fintech.md`](stacks/fintech.md)).
- **Gestion du Cycle de Vie des Tests** : Arbitrage autonome pour ajouter des tests sur les cas limites et supprimer les tests de code déprécié ([`guides/testing-strategy.md`](guides/testing-strategy.md)).

---

## 5. Configuration & Personnalisation

Toutes les préférences de votre équipe sont modifiables dans [`.agent/config.yml`](.agent/config.yml) sans altérer le Core universel :
```yaml
git:
  default_branch: "main"
  integration_branch: "developp"
  enforce_french_commits: true

security:
  dependency_audit_level: "high"
  block_on_audit_failure: true
  static_analysis_with_semgrep: true
```

---

## 6. Banc d'Évaluation & Tests Locaux

Le kit fournit sa propre suite de tests automatisés, exécutable localement sans aucun service payant ni dépendance lourde :

```bash
# 1. Tester l'intégrité globale du kit (parité, installateur, Unicode, ADR)
./scripts/test-kit.sh

# 2. Exécuter le banc d'évaluations d'agents (scénarios sécurité, fintech, méthode)
python3 scripts/run-evals.py

# 3. Vérifier la conformité stylistique et anti-slop
python3 scripts/audit-slop.py README.md guides/*.md stacks/*.md
```

---

## 7. Structure des Fichiers et Rôles

- **`core/RULES.md`** : Source unique de vérité universelle (5 phases, OWASP, clean code).
- **`presets/`** : Presets de conventions personnelles ou d'entreprise (`presets/7bhil.md`).
- **`BRAIN.md`** : Index d'orientation opérationnel de session (léger, anti-saturation de contexte).
- **`.agent/memory/`** : Mémoire contextuelle modulaire (`project.md`, `user.md`, `constraints.md`, `current-state.md`).
- **`docs/decisions/`** : Architecture Decision Records (ADR numérotés immuables).
- **`DESIGN-SYSTEM.md`** : Tokens sémantiques, accessibilité WCAG 2.2 AA et les 4 états de chaque composant UI.
- **`guides/`** : 9 guides approfondis (onboarding codebase, sécurité, observabilité, écriture sobre).
- **`stacks/`** : 9 guides de frameworks ciblés (Node, React, Python, C++, Java, PHP, Fintech, Docker, DB).
