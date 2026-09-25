# ⚛️ Règles Senior : React, Next.js (App Router) & TypeScript

> **Sources de référence** : `references/bulletproof-react`, `references/clean-code-javascript`.

---

## 1. Découpage Modulaire par Fonctionnalité (*Feature-Driven*)
- Organiser le code dans `src/features/<nom-du-domaine>/` (`components/`, `api/`, `hooks/`, `types/`, `index.ts`).
- Ne jamais importer un sous-dossier interne d'une autre feature. Tout import passe par son `index.ts` public.

---

## 2. Server vs Client Components (Next.js App Router)
- **Par défaut : Server Component (RSC)** pour la sécurité, le SEO et la réduction du bundle JS.
- N'ajouter `'use client'` **qu'aux feuilles de l'arbre de composants** nécessitant de l'interactivité (`useState`, `useEffect`, gestionnaires d'événements `onClick`).
- Ne jamais importer de code ou secrets serveur dans un composant marqué `'use client'`.

---

## 3. Gestion des Données et d'État
- **État Serveur** : Utiliser TanStack Query (React Query) ou SWR pour le cache, le refetch en arrière-plan et la synchronisation. Ne pas réinventer de cache avec un `useEffect` artisanal.
- **Formulaires** : Validation stricte via React Hook Form + Zod (`zodResolver`).
- **Composants d'interface purs** : Pas de logique métier dans les composants de présentation atomiques.
