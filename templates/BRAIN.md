# BRAIN : Mémoire et Contexte du Projet

Ce fichier constitue la **mémoire vivante** du projet. Il consigne le contexte métier, les choix d'architecture, les conventions et les directives retenues.

---

## 1. Contexte du Projet & Objectifs
- **Nom du projet** : [Nom de l'application ou du service]
- **Description** : [Description synthétique du projet et de sa valeur métier]
- **Stack technique** : [ex: TypeScript, Node.js, Next.js, PostgreSQL, Docker]

---

## 2. Directives & Préférences de l'Équipe
- **Workflow Git** : Branches thématiques (`feature/*`, `fix/*`), commits conventionnels en français, intégration sur `developp`.
- **Qualité & Rigueur** : Typage strict, aucun type évasif (`any`), validation systématique des entrées aux frontières (Zod).
- **Design & UI** : Respect strict du Design System (`global.css` et tokens `tailwind.config`), zéro couleur codée en dur.

---

## 3. Décisions d'Architecture (ADR)
Les décisions structurantes d'architecture sont consignées dans `docs/decisions/` selon le format standard ADR.
