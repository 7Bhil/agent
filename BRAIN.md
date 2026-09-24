# 🧠 BRAIN : Suivi de l'Évolution et Mémoire du Projet

Ce fichier constitue la **mémoire vivante** du projet. Il consigne l'état d'avancement, les décisions d'architecture prises, la gestion des branches et l'évolution globale du système.

---

## 🧭 Stratégie de Branches & Workflow Git

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

## 🎨 Charte Graphique & UI (Tailwind & Global CSS)

- **Source unique de vérité visuelle** :
  - Ne jamais inventer de couleurs arbitraires en ligne ou "en dur" (`#1e293b`, `rgb(...)` dispersés dans les balises).
  - Toujours se baser sur les variables CSS définies dans `global.css` (ou `globals.css`) et les tokens configurés dans `tailwind.config.js` / `tailwind.config.ts`.
  - Respecter les classes sémantiques : `bg-primary`, `text-foreground`, `border-border`, etc.

---

## 📈 Journal des Évolutions & Décisions

### Session 1 - Initialisation du Framework Senior
- **Structure créée** : Modèle ultra-léger (< 100 Ko) avec guides spécifiques, checklists, templates multi-agents et script `install.sh`.
- **Compatibilité multi-agents** :
  - `AGENTS.md` (Universel / Windsurf / Cline)
  - `GEMINI.md` (Google Gemini / Antigravity)
  - `.github/copilot-instructions.md` (GitHub Copilot / OpenAI Codex)
  - `.cursorrules` (Cursor IDE)
  - `CLAUDE.md` (Anthropic Claude)
- **Dépôt distant** : Synchronisé sur `https://github.com/7Bhil/agent.git` (branches `main` et `developp`).
- **Ajout de la mémoire vivante** : Création du présent fichier `BRAIN.md`.
