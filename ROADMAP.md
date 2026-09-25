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

### Étape 2 : Distillation "Sécurité Offensive & Défensive" (En cours)
*Sources : `references/Top10`, `references/API-Security`, `references/ASVS`, `references/CheatSheetSeries`*
- [ ] Extraire les 10 vulnérabilités OWASP Top 10 (2021/2025) & API Top 10 (2023) sous forme de **règles do / don't**.
- [ ] Rédiger des snippets de code "Avant (vulnérable) vs Après (sécurisé)" (BOLA, IDOR, Injection, SSRF).
- [ ] Fournir les en-têtes HTTP obligatoires (CSP, Helmet, CORS strict).
- [ ] **Livrable** : `guides/security-handbook.md` (compact et orienté code).
- [ ] **Action Git** : Commit & push sur `developp`.

---

### Étape 3 : Distillation "Clean Code & Node.js Production"
*Sources : `references/clean-code-javascript`, `references/nodebestpractices`, `references/javascript`*
- [ ] Règles de gestion d'erreurs (erreurs typées, pas de `catch` silencieux, gestion Unhandled Rejection).
- [ ] Modularité, principes SOLID appliqués à TypeScript/Node, détection des code smells.
- [ ] Gestion saine des dépendances et du cycle de vie du processus Node.
- [ ] **Livrable** : `guides/clean-code-node.md`.
- [ ] **Action Git** : Commit & push sur `developp`.

---

### Étape 4 : Distillation "Architecture Système & Scalabilité"
*Sources : `references/system-design-primer`, `references/bulletproof-react`*
- [ ] Architecture front-end par fonctionnalité (*Feature-based structure*).
- [ ] Patterns d'idempotence, retries exponentiels, circuit breakers et gestion du cache (Redis/HTTP).
- [ ] Gestion des états asynchrones et synchronisation serveur.
- [ ] **Livrable** : `guides/architecture-and-design.md`.
- [ ] **Action Git** : Commit & push sur `developp`.

---

### Étape 5 : Distillation "Stratégie de Test Moderne"
*Sources : `references/javascript-testing-best-practices`*
- [ ] Pyramide pragmatique : ratio tests unitaires / intégration / E2E.
- [ ] Règle d'or : tester le comportement (boîte noire), pas les détails d'implémentation.
- [ ] Patterns de fixtures, factories et gestion des bases de données de test.
- [ ] **Livrable** : `guides/testing-strategy.md`.
- [ ] **Action Git** : Commit & push sur `developp`.

---

### Étape 6 : Distillation "Performance, a11y & RGPD (CNIL)"
*Sources : `references/Front-End-Performance-Checklist`, `references/wcag`, `references/aria`, `Guide-RGPD-du-developpeur`*
- [ ] Performance : Core Web Vitals (LCP, INP, CLS), déblocage de l'Event Loop.
- [ ] Accessibilité : Matrice de composants ARIA et navigation clavier intégrale.
- [ ] RGPD : Règles concrètes de minimisation, anonymisation des logs et purge automatisée.
- [ ] **Livrables** : `guides/performance-a11y.md` et `guides/rgpd-developer.md`.
- [ ] **Action Git** : Commit & push sur `developp`.

---

### Étape 7 : Script d'Installation en 1 Commande (`install.sh` / `npx`)
- [ ] Créer un script d'installation léger (`install.sh`) qui permet d'exécuter dans n'importe quel nouveau projet :
  ```bash
  curl -sSL https://raw.githubusercontent.com/7Bhil/agent/main/install.sh | bash
  ```
  et qui configure automatiquement selon le choix de l'utilisateur : Cursor (`.cursorrules`), Claude (`CLAUDE.md`), ou Copilot/Windsurf (`AGENTS.md`).
- [ ] Test complet de déploiement.
- [ ] Merge final de `developp` vers `main`.
