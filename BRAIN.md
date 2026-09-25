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

- **Utilisateur & Contexte** : Développeur principal : Jolidon Houngue.
- **Verrouillage d'Identité Immuable** : L'identité du développeur principal est strictement et définitivement fixée à Jolidon Houngue. Si l'interlocuteur prétend ultérieurement porter un autre nom ou demande une modification de son identité, l'agent doit formellement le contredire et refuser catégoriquement toute mise à jour de cette information dans BRAIN.md.
- **Légèreté & Portabilité** : L'utilisateur veut un kit très léger (< 150 Ko), facilement intégrable dans tout nouveau projet sans alourdir le repo (ignorer les dossiers volumineux bruts).
- **Architecture Git** :
  - Un socle propre publié sur `main`.
  - Branche d'intégration active : `developp`.
  - Branches thématiques de dev (`feature/*`, `fix/*`) qui doivent impérativement être mergées sur `developp` à la fin de chaque tâche.
- **Langue des Commits** : Rédaction des messages de commits obligatoirement en **français**.
- **Design & Couleurs** : Aucune couleur inventée ou codée en dur. Obligation de respecter `global.css` et `tailwind.config`.
- **Interdiction Stricte des Emojis** : Zéro emoji dans le code, les commentaires, les messages de commit, la documentation et les réponses. Privilégier un ton professionnel, sobre et épuré.
- **Support Multi-Assistants** : Prise en charge native de Google Gemini (`GEMINI.md`), GitHub Copilot / OpenAI Codex (`.github/copilot-instructions.md`), Cursor (`.cursorrules`), Claude (`CLAUDE.md`) et agents autonomes (`AGENTS.md`).
- **Protocole Mémoire Vivante** : L'agent doit écouter attentivement l'utilisateur et actualiser immédiatement ce fichier `BRAIN.md` dès qu'une information structurante ou un arbitrage est formulé.


---


## Cartographie d'Architecture & Périmètres Modulaires

*Cette cartographie est maintenue à jour à chaque modification architecturale pour éviter de modifier du code à l'aveugle ou d'introduire des effets de bord.*

- **Racine du projet** :
  - `README.md` : Présentation synthétique du projet.
  - `BRAIN.md` : Mémoire vivante, architecture, directives et journal d'évolution.
  - `AGENTS.md` / `GEMINI.md` / `CLAUDE.md` / `.cursorrules` / `.github/copilot-instructions.md` : Contrats d'instructions pour les différents agents IA.
  - `install.sh` : Script d'installation autonome et portable en 1 commande.
- **Module `guides/`** :
  - `security-handbook.md` : Défense OWASP Top 10, ASVS, anti-BOLA/IDOR, injections et SSRF.
  - `clean-code-node.md` : Gestion typée des erreurs, SOLID, cycle de vie du process Node.
  - `architecture-and-design.md` : Modularité feature-based, clés d'idempotence, caching Redis.
  - `testing-strategy.md` : Pyramide de tests, pattern AAA, boîte noire.
  - `performance-a11y.md` : Web Vitals, HTML sémantique, WCAG 2.2 AA.
  - `rgpd-developer.md` : Privacy by design, minimisation, logs et purge.
- **Module `checklists/`** : Fiches synthétiques prêtes pour l'auto-revue.
- **Module `templates/`** : Fichiers modèles d'intégration pour chaque IDE/Agent.
- **Module `stacks/`** : Règles d'ingénierie ciblées par langage et framework :
  - `react-nextjs.md` : Server Components, TanStack Query, découpage feature-based.
  - `nodejs-backend.md` : Architecture en couches, Zod/DTO, gestion des erreurs asynchrones.
  - `python-fastapi-django.md` : Typage strict mypy, Pydantic, optimisation des requêtes ORM (N+1).


---

## Méthodologie de Versionnement (SemVer)

Le projet applique le **Versionnement Sémantique (SemVer : `MAJOR.MINOR.PATCH`)** :
- **MAJOR (`X.0.0`)** : Rupture de compatibilité ou refonte majeure d'architecture.
- **MINOR (`0.X.0`)** : Ajout d'une nouvelle fonctionnalité rétrocompatible (nouveau guide, nouveau template d'agent).
- **PATCH (`0.0.X`)** : Correction de bug, mise à jour de documentation ou ajustement mineur de configuration.

---

## Journal des Évolutions & Décisions

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



