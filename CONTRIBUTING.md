# Guide de Contribution & Standards d'Équipe

Ce document régit les règles de contribution applicables aux développeurs et aux agents d'ingénierie intervenant sur ce dépôt.

---

## 1. Principes Généraux
- **Poste d'Ingénieur Senior** : Rigueur d'investigation, pas de suppositions non vérifiées, zéro complaisance avec la dette technique.
- **Sobriété et Lisibilité** : Éviter toute sur-ingénierie (KISS, YAGNI). Le code doit être auto-porteur, explicite et typé sans ambiguïté.
- **Règle de chesterton** : Ne jamais supprimer ou altérer un composant existant sans en maîtriser la raison d'être historique.

---

## 2. Cycle de Travail Git
Les conventions de branches et de commits sont définies dans `.agent/config.yml` (paramétrable par projet).
1. **Création de Branche** :
   - Branche d'intégration : configurée via `git.integration_branch` (par défaut `developp`).
   - Branche de travail : `feature/<nom-fonctionnalite>`, `fix/<nom-correctif>`, `refactor/<nom-refactoring>`.
2. **Messages de Commit** :
   - Rédigés selon la configuration active (`git.enforce_french_commits` et `git.convention`).
   - Format conventionnel : `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`, `test: ...`, `chore: ...`.
   - Zéro émoji dans les messages de commit.
3. **Revue et Intégration** :
   - Validation locale préalable : `./scripts/test-kit.sh` et `python3 scripts/run-evals.py`.
   - Fusion systématique sur la branche d'intégration définie.

---

## 3. Garde-fous Techniques Incompressibles
- **Typage Strict** : Bannissement intégral du type `any` et des assertions non sécurisées (`as unknown as T`).
- **Design System** : Utilisation exclusive des classes sémantiques et des variables définies dans `global.css` et `tailwind.config`. Aucune couleur inventée ou codée en dur.
- **Décisions Structurantes** : Tout arbitrage technique majeur doit faire l'objet d'un Architecture Decision Record dans `docs/decisions/`.
- **Rédaction Sobre** : Respecter les règles anti-slop définies dans `guides/clean-technical-writing.md`.

---

## 4. Checklist Avant Soumission
- [ ] La suite de tests passe intégralement au vert.
- [ ] Le linter et la vérification de types (`tsc --noEmit`) ne rapportent aucune erreur.
- [ ] L'audit de sécurité des dépendances ne rapporte aucune vulnérabilité de niveau critique ou élevé.
- [ ] L'audit de rédaction technique (`python3 scripts/audit-slop.py`) est validé.
- [ ] Le fichier `BRAIN.md` ou l'ADR correspondant a été mis à jour.
