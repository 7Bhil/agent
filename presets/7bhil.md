# Préférences Utilisateur et Conventions Spécifiques : 7Bhil

Ce fichier documente le profil et les préférences retenues pour le compte et les projets de **7Bhil**.
Ces préférences s'appliquent en complément des règles universelles de `core/RULES.md` et sont configurées par défaut dans `.agent/config.yml`.

---

## 1. Conventions Git & Intégration
- **Langue des Commits** : Rédigés obligatoirement en **français**, préfixés par convention (`feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`, `test: ...`, `style: ...`, `chore: ...`).
- **Stratégie de Branches** :
  - Branche principale de publication / production : `main`.
  - Branche d'intégration continue de développement : `developp`.
  - Branches de travail thématiques : `feature/*`, `fix/*`, `refactor/*`.
  - Toute branche de travail terminée et validée est fusionnée par merge commit (`--no-ff`) sur `developp`.

---

## 2. Style, UI & Identité Visuelle
- **Source unique de vérité** : Variables CSS configurées dans `global.css` (ou `globals.css`) et tokens déclarés dans `tailwind.config.ts` / `tailwind.config.js`.
- **Zéro couleur codée en dur** : Aucune chaîne hexadécimale arbitraire ou rgb en dur dans les composants.
- **Sobriété d'Entreprise** : Interfaces épurées, typographie sans-serif neutre, composants basés sur Radix UI / shadcn/ui.

---

## 3. Sobriété Textuelle & Zéro Émoji
- **Interdiction formelle des émojis** : Aucun émoji dans le code, les commentaires, la documentation, les messages de commit ou les réponses conversationnelles.
- **Rédaction Anti-Slop** : Proscription des formules creuses, du hedging (*"il convient de noter"*), de la fausse connivence et de l'emphase dramatique. Contrôle via `scripts/audit-slop.py`.

---

## 4. Stacks Techniques Privilégiées
- Front-end : Next.js (App Router, Server Components), Tailwind CSS, TanStack Query.
- Mobile : React Native / Expo.
- Backend : Node.js (NestJS / Express) avec typage strict TypeScript, ou Python (FastAPI / Pydantic v2).
- Persistance & Données : PostgreSQL, Prisma / Drizzle, modélisation 3NF et conformité ACID.
- Fintech & Paiement : Unités mineures entières, grand livre à double entrée, intégration Mobile Money (FedaPay, KKiaPay) avec webhooks signés.
