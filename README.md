# Senior Agent Core (`agent-senior`)

> **Kit ultra-léger et portable** pour transformer instantanément n'importe quel agent d'IA (Cursor, Claude, Windsurf, Copilot, ChatGPT) en **Ingénieur Logiciel Senior**.

Ce kit synthétise l'essentiel des meilleures références mondiales en ingénierie logicielle :
- **OWASP Top 10** (2021 & 2025)
- **OWASP API Security Top 10** (2023)
- **OWASP ASVS 4.0** & **Cheat Sheet Series**
- **System Design Primer** (Scalabilité, Résilience, Caching)
- **Bulletproof React** (Architecture front-end scalable)
- **Clean Code JavaScript** & **Node.js Best Practices** (Goldbergyoni)
- **JavaScript Testing Best Practices** (Pyramide de tests, AAA, boîte noire)
- **Front-End Performance Checklist** & **WCAG 2.2 / WAI-ARIA**
- **Guide RGPD du Développeur (CNIL)**

---

## 🚀 Utilisation Rapide dans Vos Projets

Pour équiper un projet d'un agent senior, copiez simplement l'un des fichiers suivants à la racine de votre projet :

1. **Pour tout agent IA universel** : Copiez [`AGENTS.md`](./AGENTS.md)
2. **Pour Cursor** : Copiez [`templates/.cursorrules`](./templates/.cursorrules) sous `.cursorrules`
3. **Pour Claude / Anthropic** : Copiez [`templates/CLAUDE.md`](./templates/CLAUDE.md)

---

## 🧭 Le Cœur : Les 4 Piliers Senior

1. **Investigation d'abord** : Identifier la cause racine avant d'écrire la moindre ligne de code. Zéro régression.
2. **Clean Architecture & SOLID** : Séparation stricte domaine / transport / persistance.
3. **Sécurité par Défaut** : Protection BOLA/IDOR systématique, validation Zod, zéro secret dans les logs.
4. **Tests Comportementaux** : Pattern Arrange-Act-Assert, priorité aux tests d'intégration et tests aux limites.

---

## 🌿 Branches Git

- `main` : Socle stable et léger prêt à l'emploi.
- `developp` : Enrichissement progressif des modules et synthèses détaillées.
