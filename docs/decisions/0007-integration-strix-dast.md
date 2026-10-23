# ADR 0007 : Intégration de Strix pour les Tests d'Intrusion Dynamiques (DAST)

- **Statut** : Accepté
- **Date** : 2026-10-23
- **Auteur** : 7Bhil / Antigravity

---

## 1. Contexte

Le kit Senior Agent Core disposait jusqu'alors d'outils d'analyse statique défensive (Semgrep pour le code, Gitleaks pour les secrets) et de règles d'architecture rigoureuses.
Cependant, l'analyse statique génère des faux positifs et ne teste pas la logique applicative dynamique (BOLA/IDOR complexes, interactions d'API ou failles de flux).

L'émergence d'agents autonomes d'audit offensif comme **Strix** (`usestrix/strix`) permet d'exécuter des tests d'intrusion dynamiques et de produire des preuves d'exploitation concrètes (Proof of Concept - PoC).

## 2. Décision

1. **Gabarit de Workflow CI/CD (`templates/.github/workflows/strix-security.yml`)** :
   - Ajout d'un workflow GitHub Actions pour exécuter Strix en mode différentiel (`--scope-mode diff`) lors des pull requests.
   - Protection contre l'échec en l'absence de clé API LLM (scan ignoré proprement si le secret n'est pas renseigné).
2. **Intégration au guide de sécurité et aux checklists** :
   - Mise à jour de `.agent/guides/security-handbook.md` (section 4 : tests d'intrusion dynamiques).
   - Mise à jour de `.agent/checklists/03-securite-applicative-et-api.md`.
3. **Déploiement via `install.sh`** :
   - Prise en charge du déploiement du workflow de sécurité dans les projets clients.

## 3. Conséquences

- **Positives** :
  - Détection proactive et dynamique des failles de logique métier avant mise en production.
  - Zéro dépendance locale forcée : Strix s'exécute dans l'infrastructure de CI ou via un outil CLI externe sans alourdir le kit de base.
- **Vigilance** :
  - Nécessite de configurer un secret LLM (`STRIX_LLM_API_KEY` ou équivalent) dans le dépôt GitHub pour activer l'audit automatisé.
