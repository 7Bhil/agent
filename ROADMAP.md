# Feuille de Route : Construction du Kit "Senior Agent"

Cette roadmap planifie l'extraction méthodique des **2 262 fichiers de références** rassemblés dans `references/` pour les distiller en règles compactes, pragmatiques et prêtes à l'emploi pour tout agent d'IA.

---

## Objectif
Créer un kit ultra-léger (< 150 Ko) intégrable dans n'importe quel nouveau projet (`git clone` ou simple copie de dossier), garantissant qu'un agent IA respecte les standards d'un ingénieur senior sans halluciner ni introduire de régression ou faille de sécurité.

---

## Les 7 Étapes de Travail

### Étape 1 : Fondations & Déploiement Initial (Terminé)
- [x] Initialisation du dépôt Git avec `.gitignore` ciblé (références lourdes exclues).
- [x] Publication du socle minimal sur `main`.
- [x] Publication des premières fiches d'orientation sur `developp`.
- [x] Configuration du remote distant GitHub (`7Bhil/agent.git`).

---

### Étape 2 : Distillation "Sécurité Offensive & Défensive" (Terminé)
*Sources : `references/Top10`, `references/API-Security`, `references/ASVS`, `references/CheatSheetSeries`*
- [x] Extraire les 10 vulnérabilités OWASP Top 10 (2021/2025) & API Top 10 (2023) sous forme de **règles do / don't**.
- [x] Rédiger des snippets de code "Avant (vulnérable) vs Après (sécurisé)" (BOLA, IDOR, Injection, SSRF).
- [x] Fournir les en-têtes HTTP obligatoires (CSP, Helmet, CORS strict).
- [x] **Livrable** : `guides/security-handbook.md` (compact et orienté code).
- [x] **Action Git** : Commit & push sur `developp`.

---

### Étape 3 : Distillation "Clean Code & Node.js Production" (Terminé)
*Sources : `references/clean-code-javascript`, `references/nodebestpractices`, `references/javascript`*
- [x] Règles de gestion d'erreurs (erreurs typées, pas de `catch` silencieux, gestion Unhandled Rejection).
- [x] Modularité, principes SOLID appliqués à TypeScript/Node, détection des code smells.
- [x] Gestion saine des dépendances et du cycle de vie du processus Node.
- [x] **Livrable** : `guides/clean-code-node.md`.
- [x] **Action Git** : Commit & push sur `developp`.

---

### Étape 4 : Distillation "Architecture Système & Scalabilité" (Terminé)
*Sources : `references/system-design-primer`, `references/bulletproof-react`*
- [x] Architecture front-end par fonctionnalité (*Feature-based structure*).
- [x] Patterns d'idempotence, retries exponentiels, circuit breakers et gestion du cache (Redis/HTTP).
- [x] Gestion des états asynchrones et synchronisation serveur.
- [x] **Livrable** : `guides/architecture-and-design.md`.
- [x] **Action Git** : Commit & push sur `developp`.

---

### Étape 5 : Distillation "Stratégie de Test Moderne" (Terminé)
*Sources : `references/javascript-testing-best-practices`*
- [x] Pyramide pragmatique : ratio tests unitaires / intégration / E2E.
- [x] Règle d'or : tester le comportement (boîte noire), pas les détails d'implémentation.
- [x] Patterns de fixtures, factories et gestion des bases de données de test.
- [x] **Livrable** : `guides/testing-strategy.md`.
- [x] **Action Git** : Commit & push sur `developp`.

---

### Étape 6 : Distillation "Performance, a11y & RGPD (CNIL)" (Terminé)
*Sources : `references/Front-End-Performance-Checklist`, `references/wcag`, `references/aria`, `Guide-RGPD-du-developpeur`*
- [x] Performance : Core Web Vitals (LCP, INP, CLS), déblocage de l'Event Loop.
- [x] Accessibilité : Matrice de composants ARIA et navigation clavier intégrale.
- [x] RGPD : Règles concrètes de minimisation, anonymisation des logs et purge automatisée.
- [x] **Livrables** : `guides/performance-a11y.md` et `guides/rgpd-developer.md`.
- [x] **Action Git** : Commit & push sur `developp`.

---

### Étape 7 : Script d'Installation en 1 Commande (`install.sh` / `npx`) (Terminé)
- [x] Créer un script d'installation léger (`install.sh`) qui permet d'exécuter dans n'importe quel nouveau projet :
  ```bash
  curl -sSL https://raw.githubusercontent.com/7Bhil/agent/main/install.sh | bash
  ```
  et qui configure automatiquement selon le choix de l'utilisateur : Cursor (`.cursorrules`), Claude (`CLAUDE.md`), ou Copilot/Windsurf (`AGENTS.md`).
- [x] Test complet de déploiement.
- [x] Merge final de `developp` vers `main`.

