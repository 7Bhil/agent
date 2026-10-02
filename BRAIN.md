# BRAIN : Suivi de l'Évolution et Mémoire du Projet

Ce fichier constitue la **mémoire vivante** du projet. Il consigne l'état d'avancement, les décisions d'architecture prises, la gestion des branches et l'évolution globale du système.

---

## Stratégie de Branches & Workflow Git

- **`main`** : Branche de production / version stable finale.
- **`developp`** : Branche principale d'intégration. Tout travail terminé est mergé sur `developp`.
- **Branches de travail (`feature/*`, `fix/*`, `refactor/*`)** :
  - Tout développement s'effectue sur une branche dédiée (ex: `feature/auth-guard`, `feature/dark-mode`).
  - **À la fin de la tâche**, la branche est testée puis **fusionnée (merged) sur `developp`**.
- **Messages de Commit** :
  - Rédigés **exclusivement en français**, préfixés par convention :
    - `feat: ...` (ajout d'une fonctionnalité)
    - `fix: ...` (correction de bug)
    - `docs: ...` (documentation)
    - `refactor: ...` (refactorisation sans changement de comportement)
    - `test: ...` (tests unitaires / intégration)
    - `style: ...` (mise en page, styles CSS / Tailwind)

---

## Charte Graphique & UI (Tailwind & Global CSS)

- **Source unique de vérité visuelle** :
  - Ne jamais inventer de couleurs arbitraires en ligne ou "en dur" (`#1e293b`, `rgb(...)` dispersés dans les balises).
  - Toujours se baser sur les variables CSS définies dans `global.css` (ou `globals.css`) et les tokens configurés dans `tailwind.config.js` / `tailwind.config.ts`.
  - Respecter les classes sémantiques : `bg-primary`, `text-foreground`, `border-border`, etc.

---

## Directives & Préférences Utilisateur Retenues

*Cette section est alimentée en continu par l'agent au fil des échanges. Tout retour critique, choix imposé, habitude ou consigne formulée par l'utilisateur doit être consigné ici pour être respecté dans toutes les sessions suivantes.*

- **Légèreté & Portabilité** : L'utilisateur veut un kit très léger (< 150 Ko), facilement intégrable dans tout nouveau projet sans alourdir le repo (ignorer les dossiers volumineux bruts).
- **Architecture Git** :
  - Un socle propre publié sur `main`.
  - Branche d'intégration active : `developp`.
  - Branches thématiques de dev (`feature/*`, `fix/*`) qui doivent impérativement être mergées sur `developp` à la fin de chaque tâche.
- **Langue des Commits** : Rédaction des messages de commits obligatoirement en **français**.
- **Design & Couleurs** : Aucune couleur inventée ou codée en dur. Obligation de respecter `global.css` et `tailwind.config`.
- **Interdiction Stricte des Emojis** : Zéro emoji dans le code, les commentaires, les messages de commit, la documentation et les réponses. Privilégier un ton professionnel, sobre et épuré.
- **Sobriété Rédactionnelle & Anti-Slop IA** : Interdiction du remplissage artificiel, des formules creuses de hedging, des fausses connivences, de l'emphase dramatique et des conclusions résumatives superflues. Contrôle automatisé déterministe via `scripts/audit-slop.py`.
- **Support Multi-Assistants** : Prise en charge native de Google Gemini (`GEMINI.md`), GitHub Copilot / OpenAI Codex (`.github/copilot-instructions.md`), Cursor (`.cursorrules`), Claude (`CLAUDE.md`) et agents autonomes (`AGENTS.md`).
- **Protocole Mémoire Vivante** : L'agent doit écouter attentivement l'utilisateur et actualiser immédiatement ce fichier `BRAIN.md` dès qu'une information structurante ou un arbitrage est formulé.


---


## Cartographie d'Architecture & Périmètres Modulaires

*Cette cartographie est maintenue à jour à chaque modification architecturale pour éviter de modifier du code à l'aveugle ou d'introduire des effets de bord.*

- **Racine du projet** :
  - `README.md` : Présentation synthétique du projet.
  - `DESIGN.md` : Cadre du Design System, palette sémantique, typographie, espacements et 4 états d'interface.
  - `CONTRIBUTING.md` : Guide des normes de contribution d'équipe et standards seniors.
  - `BRAIN.md` : Mémoire vivante, architecture, directives et journal d'évolution.
  - `AGENTS.md` / `GEMINI.md` / `CLAUDE.md` / `.cursorrules` / `.github/copilot-instructions.md` : Contrats d'instructions pour les différents agents IA.
  - `.semgrep.yml` : Règles d'analyse statique de sécurité (injections SQL, secrets en dur, logs production).
  - `.agent/config.yml` : Configuration paramétrable et débrayable des règles du kit.
  - `install.sh` : Script d'installation autonome et portable en 1 commande.
- **Module `docs/decisions/` (ADR)** :
  - `README.md` : Modèle et standardisation des Architecture Decision Records.
  - `0001-adoption-du-format-adr-et-decouplage-memoire.md` : Arbitrage formel d'adoption des ADR pour l'équipe.
- **Module `.github/`** :
  - `CODEOWNERS` : Définition des responsabilités par module.
  - `pull_request_template.md` : Gabarit de PR avec checklist d'auto-revue obligatoire.
  - `workflows/ci.yml` : Pipeline d'intégration continue interne du kit.
- **Module `scripts/`** :
  - `audit-slop.py` : Outil déterministe autonome (Python stdlib pur, zéro dépendance) détectant les tics de langage et le remplissage IA en français et anglais.
  - `setup-git-hooks.sh` : Script d'installation automatique des hooks Git locaux (`commit-msg` conventionnel et `pre-commit` anti-slop).
- **Module `guides/`** :
  - `onboard-codebase.md` : Protocole Phase 0 de prise en main de l'existant, génération de CODEMAP, traçage de flux et tests de caractérisation.
  - `clean-technical-writing.md` : Guide de rédaction technique sobre, concision active et anti-slop IA.
  - `observability-and-logging.md` : Observabilité, format JSON structuré, OpenTelemetry, Google SRE Golden Signals et sondes liveness/readiness.
  - `security-handbook.md` : Défense OWASP Top 10, ASVS, anti-BOLA/IDOR, injections et SSRF.
  - `clean-code-node.md` : Gestion typée des erreurs, SOLID, cycle de vie du process Node.
  - `architecture-and-design.md` : Modularité feature-based, clés d'idempotence, caching Redis.
  - `testing-strategy.md` : Pyramide de tests, pattern AAA, boîte noire.
  - `performance-a11y.md` : Web Vitals, HTML sémantique, WCAG 2.2 AA.
  - `rgpd-developer.md` : Privacy by design, minimisation, logs et purge.
- **Module `checklists/`** :
  - `01-architecture-et-conception.md` à `06-performance-et-accessibilite.md` : Fiches synthétiques d'auto-revue.
  - `07-redaction-technique-anti-slop.md` : Grille d'auto-revue de prose technique et élimination des artefacts IA.
- **Module `templates/`** : Fichiers modèles d'intégration pour chaque IDE/Agent, CI/CD et gestion d'environnement (synchronisation stricte testée en CI).
- **Module `stacks/`** : Règles d'ingénierie ciblées par langage et framework :
  - `docker-containerization.md` : Durcissement Docker, multi-stage builds, utilisateur non-root et gestion du PID 1.
  - `react-nextjs.md` : Server Components, Next.js Edge Runtime, Caching, Middleware, TanStack Query.
  - `nodejs-backend.md` : Architecture en couches, NestJS (Modules, Decorators, Scopes), Express et gestion d'erreurs asynchrones.
  - `python-fastapi-django.md` : Typage strict mypy, Pydantic V2, FastAPI (Depends), Django (Middlewares, ORM N+1).
  - `cpp.md` : C & C++ moderne, RAII, smart pointers, C++20 concepts, CMake moderne (Target-based).
  - `java-spring.md` : Java 17/21 LTS, Spring Boot 3, IoC par constructeur, JPA/Hibernate (anti N+1), DTO records, JUnit 5.
  - `laravel-php.md` : PHP 8.2+, Laravel 10/11, Form Requests, Service Container, Eloquent scopes, queues asynchrones.
  - `database-management.md` : Modélisation SQL/NoSQL transverse, normalisation 3NF, indexation sélective, ACID, pattern Expand/Contract.
  - `fintech.md` : Systèmes financiers et Mobile Money, unités mineures, grand livre à double entrée, idempotence et webhooks signés.


---

## Méthodologie de Versionnement (SemVer)

Le projet applique le **Versionnement Sémantique (SemVer : `MAJOR.MINOR.PATCH`)** :
- **MAJOR (`X.0.0`)** : Rupture de compatibilité ou refonte majeure d'architecture.
- **MINOR (`0.X.0`)** : Ajout d'une nouvelle fonctionnalité rétrocompatible (nouveau guide, nouveau template d'agent).
- **PATCH (`0.0.X`)** : Correction de bug, mise à jour de documentation ou ajustement mineur de configuration.

---

## Journal des Évolutions & Décisions

### [2.7.0] - Outillage de Sécurité Statique (Semgrep, Gitleaks) & Configuration Débrayable
- **Configuration Débrayable Universelle** : Création de `.agent/config.yml` permettant d'ajuster les conventions d'équipe (langue des commits, branches d'intégration, niveau d'audit de sécurité, contrôle anti-slop).
- **Analyse Statique Automatisée (Semgrep)** : Création de `.semgrep.yml` avec règles ciblées pour JavaScript/TypeScript (détection des secrets JWT en dur, concaténation de requêtes SQL non sécurisées, `console.log` en production).
- **Protection Anti-Fuite de Secrets** : Intégration de `gitleaks protect --staged` dans le hook `pre-commit` automatisé via `scripts/setup-git-hooks.sh`.
- **Mise à Jour du Déploiement** : Intégration de `.agent/config.yml` et `.semgrep.yml` dans `install.sh`.

### [2.6.0] - Direction Artistique Positive (DESIGN.md) & Stack Spécialisée Fintech
- **Direction Artistique & Design System** :
  - Création de `DESIGN.md` avec charte sémantique, variables CSS HSL, typographie sans-serif propre, règles WCAG 2.2 AA.
  - Formalisation des 4 états obligatoires de chaque composant d'interface (Loading avec skeleton, Nominal, Empty state avec action, Error avec retry).
- **Ingénierie Financière & Fintech** :
  - Création de `stacks/fintech.md` traitant des contraintes critiques : bannissement des nombres à virgule flottante, manipulation en unités mineures entières, grand livre immuable à double entrée (*Double-Entry Ledger*).
  - Architecture d'intégration Mobile Money (FedaPay, KKiaPay, MTN, Moov, Orange) : vérification cryptographique HMAC en temps constant, découplage asynchrone des webhooks et réconciliation automatique.
- **Mise à Jour de l'Installation** : Intégration de `DESIGN.md` et `stacks/fintech.md` dans `install.sh`.

### [2.5.0] - Standardisation ADR & Outillage Collaboratif d'Équipe
- **Système d'Architecture Decision Records (ADR)** :
  - Création de `docs/decisions/README.md` avec formalisation du gabarit d'arbitrage.
  - Création de `docs/decisions/0001-adoption-du-format-adr-et-decouplage-memoire.md` officialisant le découplage entre mémoire courte et décisions de fond.
- **Cadre de Contribution & Équipe** :
  - Création de `CONTRIBUTING.md` (cycle Git, conventions en français, règles incompressibles et checklist).
  - Création de `.github/CODEOWNERS` pour attribuer la gouvernance technique par module.
  - Création de `.github/pull_request_template.md` avec grille de contrôle senior (Phase 0, typage, tests, sécurité, design).
- **Sobriété et Contrôle Déterministe** : Zéro tic IA et validation de `audit-slop.py`.

### [2.4.1] - Correction Critique du Déploiement et Découplage de la CI
- **Déploiement Intégral dans `install.sh`** : Installation automatique de tous les guides (`guides/` et `.agent/guides/`), des checklists (`checklists/` et `.agent/checklists/`) et de l'ensemble des stacks techniques (`stacks/` et `.agent/stacks/`).
- **Initialisation Automatique de la Mémoire** : Déploiement d'un modèle propre `templates/BRAIN.md` si aucun `BRAIN.md` n'existe dans le projet cible.
- **Découplage de la CI Déployée** : Création de `templates/.github/workflows/ci.yml` et fiabilisation de `templates/.gitlab-ci.yml` (suppression de l'attente de `templates/` inexistant chez le client, vérification de `package.json` avant `setup-node`, scan dynamique des dossiers documentaires).
- **Rigueur Sécurité Dépendances** : Suppression du contournement `|| true` sur `npm audit --audit-level=high` dans `.github/workflows/ci.yml` et `templates/.github/workflows/ci.yml`.

### [2.4.0] - Intégration du Protocole Phase 0 Onboarding & Exploration de l'Existant
- **Protocole d'Onboarding & Exploration** : Création de `guides/onboard-codebase.md` définissant les 5 étapes d'investigation préalable (génération de `CODEMAP.md`, baseline test run, traçage de flux bout en bout, archéologie Git via `git blame`/`log`, tests de caractérisation).
- **Enrichissement du Contrat d'Agent (5 Phases)** : Insertion formelle de la Phase 0 dans `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules` et `templates/.github/copilot-instructions.md`.
- **Alignement strict des templates** : Synchronisation des fichiers miroirs dans `templates/`.
- **Audit de style & slop validé** : Zéro tic IA et zéro emoji sur l'ensemble de la documentation.

### [2.3.0] - Observabilité Industrielle, Durcissement Docker & Automatisation des Git Hooks
- **Observabilité & Télémétrie** : Création de `guides/observability-and-logging.md` (logs JSON structurés, corrélation distribuée, signaux SRE et découplage liveness/readiness/startup).
- **Conteneurisation sécurisée** : Création de `stacks/docker-containerization.md` (multi-stage builds, non-root par défaut, gestion PID 1 avec tini, read-only rootfs).
- **Automatisation Git Hooks** : Création de `scripts/setup-git-hooks.sh` installant `commit-msg` (format conventionnel strict en français + interdiction des émojis) et `pre-commit` (audit automatique anti-slop sur les fichiers indexés).
- **Résolution de la redondance `templates/`** : Synchronisation stricte et ajout d'un test automatisé de parité (`cmp`) dans `.github/workflows/ci.yml` et `.gitlab-ci.yml`.
- **Intégration dans `install.sh`** : Déploiement et activation automatique des hooks Git lors de l'installation du kit.

### [2.2.0] - Expansion Universelle des Stacks Techniques & Harmonisation Racine
- **Harmonisation structurelle racine** : Déploiement direct de `GEMINI.md`, `CLAUDE.md` et `.cursorrules` à la racine du projet pour une auto-documentation immédiate dans tous les environnements d'IA.
- **Nouvelles stacks techniques** :
  - `stacks/cpp.md` : C/C++ moderne, RAII, gestion mémoire smart pointers et CMake target-based.
  - `stacks/java-spring.md` : Java 17/21, Spring Boot 3, IoC constructeur, JPA sans N+1, records immutables et tests réels.
  - `stacks/laravel-php.md` : Laravel 10/11, Form Requests, injection de dépendances, Eloquent sans requêtes paresseuses.
  - `stacks/database-management.md` : Guide transverse SQL/NoSQL (indexation, ACID, migrations sans interruption de service).
- **Enrichissement des stacks existantes** :
  - `stacks/nodejs-backend.md` : NestJS approfondi (modules, injection, pipes, guards) et Express.
  - `stacks/python-fastapi-django.md` : FastAPI (`Depends`, async vs sync) et Django (middlewares, optimisation ORM).
  - `stacks/react-nextjs.md` : Next.js App Router, Edge runtime, revalidation de cache et middlewares.
- **Amélioration de l'outillage** :
  - `scripts/audit-slop.py` enrichi avec détection des tournures passives lourdes et répétitions mécaniques.
  - `install.sh` réaligné pour télécharger les fichiers d'agents directement depuis la racine.
- **Feuille de route** : Validation et clôture de l'Étape 8 dans `ROADMAP.md`.

### [2.1.0] - Intégration de la Charte de Rédaction Technique & Outillage Déterministe Anti-Slop IA
- **Absorption des meilleures pratiques anti-slop** : Synthèse opérationnelle inspirée de `humanize-skill` et `de-slop`.
- **Nouveau guide d'ingénierie** : Création de `guides/clean-technical-writing.md` définissant les principes de concision active, élimination du hedging et modes préservation/conforme.
- **Nouvelle checklist d'auto-revue** : Ajout de `checklists/07-redaction-technique-anti-slop.md`.
- **Outil autonome sans dépendance** : Implémentation de `scripts/audit-slop.py` (Python 3 stdlib pur) avec règles bilingues (FR/EN) et test unitaire interne (`--selftest`).
- **Pipeline CI & Templates** : Intégration du contrôle d'audit dans GitHub Actions (`.github/workflows/ci.yml`), GitLab CI (`templates/.gitlab-ci.yml`) et mise à jour d'`install.sh`.
- **Mise à jour des contrats d'agents** : Propagation de la clause de sobriété rédactionnelle dans `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules` et `copilot-instructions.md`.
- **Validation globale** : Zéro emoji et zéro faux positif sur l'ensemble de la documentation du dépôt.

### [2.0.0] - Publication Majeure du Senior Agent Core & Clôture de la Roadmap
- **Achèvement intégral des 7 étapes de la Roadmap** : Tous les livrables d'ingénierie senior sont produits, testés et vérifiés.
- **Documentation et commande d'installation** : `README.md` et `install.sh` finalisés pour permettre un déploiement universel depuis la branche stable `main`.
- **Zéro émoji et esthétique sobre validés** : Vérification binaire automatisée de pureté textuelle.
- **Fusion et synchronisation** : Intégration globale de `developp` vers `main`.

### [1.9.0] - Purge et Éradication Totale des Émojis

- **Assainissement complet du dépôt** : Suppression de chaque émoji présent dans les fichiers Markdown, scripts bash, configurations CI et templates.
- **Vérification binaire automatisée** : Exécution d'un script de scan Unicode validant zéro émoji détecté sur l'intégralité du projet.

### [1.8.0] - Support des Issues et Modèles de Traçabilité

- **Gabarits d'Issues GitHub** : Ajout de `.github/ISSUE_TEMPLATE/bug_report.md` et `feature_request.md` pour cadrer la formalisation des tâches.
- **Rôle de l'IA sur les Issues** : L'IA peut rédiger, diagnostiquer ou soumettre des issues directement via l'API GitHub ou la CLI `gh` lors des audits et investigations.

### [1.7.0] - Verrouillage Anti-Style IA & Esthétique Entreprise

- **Bannissement des styles "IA génériques"** : Interdiction absolue des dégradés fluo/violet/indigo arbitraires, des bordures lumineuses et du glassmorphism forcé non demandé.
- **Respect strict du Design System** : Utilisation exclusive des classes Tailwind sémantiques et des variables de `global.css`.
- **Zéro Emoji garanti** : Verrouillage formel dans l'ensemble des instructions d'agents pour éliminer tout déchet visuel.

### [1.6.0] - Règle de Sobriété Formelle & Zéro Emoji

- **Bannissement intégral des émojis** : Interdiction stricte d'utiliser des émojis dans le code, les commentaires, la documentation, les messages de commits et les réponses textuelles.
- **Rigueur d'ingénierie** : Ton épuré, sobre et professionnel exigé de tous les agents.
- **Propagation universelle** : Consigne inscrite dans `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules`, `copilot-instructions.md` et `BRAIN.md`.

### [1.5.0] - Modules d'Ingénierie par Stack Technique (`stacks/`)

- **Création du module `stacks/`** : Règles ciblées pour les frameworks majeurs afin d'éviter les idiomes obsolètes :
  - `stacks/react-nextjs.md` : RSC vs Client components, TanStack Query, découpage feature-based.
  - `stacks/nodejs-backend.md` : Découplage Controllers/Services/DAL, Graceful shutdown.
  - `stacks/python-fastapi-django.md` : Typage strict, prévention du N+1 ORM, Pydantic v2.
- **Principe d'auto-adaptation** : L'agent audite les fichiers de config du projet (`package.json`, `requirements.txt`) et applique spontanément les règles de la stack correspondante.

### [1.4.0] - Template de Sécurité des Secrets (`.env.example`)

- **Protection des Secrets & Zero Leak** : Ajout du gabarit `templates/.env.example` pour cadrer la configuration d'environnement dès le démarrage d'un projet et empêcher les fuites de secrets dans Git.
- **Intégration dans `install.sh`** : Déploiement automatique du modèle `.env.example` lors de l'initialisation d'un projet s'il n'existe pas déjà.

### [1.3.0] - Protocole d'Auto-Discipline & Autonomie Totale de l'Agent

- **Clause de Proactivité Autonome** : L'agent a l'interdiction d'attendre que l'utilisateur lui rappelle les règles. Il doit s'auto-discipliner dès la première seconde.
- **Règle du Premier Réflexe** : Consultation obligatoire de `BRAIN.md`, diagnostic de la cause racine avant d'écrire du code, zéro dette, commits en français, merge sur `developp` et mise à jour finale de `BRAIN.md` sans intervention de l'utilisateur.
- **Propagation universelle** : Règle injectée dans `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `.cursorrules` et `copilot-instructions.md`.

### [1.2.0] - Garde-fous Anti-Hallucination, Refus de Dette Technique & Pipelines CI (GitHub Actions / GitLab CI)

- **Pipelines CI automatiques** :
  - Création de `.github/workflows/ci.yml` (lint, tsc strict, tests unitaires, audit npm, contrôle de présence obligatoire de `BRAIN.md`).
  - Création de `templates/.gitlab-ci.yml` pour les projets hébergés sur GitLab.
- **Règles Anti-Hallucination Formelles** :
  - Interdiction absolue pour un agent d'inventer des packages, méthodes ou signatures. Obligation d'inspecter les sources et `package.json`.
- **Tolérance Zéro pour la Dette Technique** :
  - Interdiction du type `any`, pas de code mort/orphelin, pas de hacks temporaires non documentés. Tests obligatoires pour tout changement.
- **Mise à jour d'`install.sh`** : Déploiement automatique des pipelines CI dans les nouveaux projets.

### [1.1.0] - Versionnement clair, Cartographie d'Architecture & Règle Stricte des Commits en Français
- **Cartographie d'Architecture** : Enregistrement de la cartographie complète dans `BRAIN.md` pour éviter les modifications hasardeuses.
- **Règle absolue des commits** : Obligation inconditionnelle de rédiger 100 % des commits en **français**.
- **Méthodologie SemVer** : Formalisation du versionnement pour chaque étape du travail.

### [1.0.0] - Initialisation du Framework Senior
- **Structure créée** : Modèle ultra-léger (< 100 Ko) avec guides spécifiques, checklists, templates multi-agents et script `install.sh`.
- **Compatibilité multi-agents** : `AGENTS.md`, `GEMINI.md`, `.github/copilot-instructions.md`, `.cursorrules`, `CLAUDE.md`.
- **Dépôt distant** : Synchronisé sur `https://github.com/7Bhil/agent.git` (branches `main` et `developp`).
- **Mémoire vivante & apprentissage continu** : Mise en place du protocole d'écoute continue des consignes utilisateur.



