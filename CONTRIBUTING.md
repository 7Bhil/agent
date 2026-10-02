# Guide de Contribution & Standards d'Équipe

Ce document régit les règles de contribution applicables aux développeurs et aux agents d'ingénierie intervenant sur ce dépôt.

---

## 1. Principes Généraux
- **Poste d'Ingénieur Senior** : Rigueur d'investigation, pas de suppositions non vérifiées, zéro complaisance avec la dette technique.
- **Sobriété et Lisibilité** : Éviter toute sur-ingénierie (KISS, YAGNI). Le code doit être auto-porteur, explicite et typé sans ambiguïté.
- **Règle de chesterton** : Ne jamais supprimer ou altérer un composant existant sans en maîtriser la raison d'être historique.

---

## 2. Cycle de Travail Git
1. **Création de Branche** :
   - Branche d'intégration : `developp`.
   - Branche de travail : `feature/<nom-fonctionnalite>`, `fix/<nom-correctif>`, `refactor/<nom-refactoring>`.
2. **Messages de Commit** :
   - Rédigés obligatoirement en **français**.
   - Format conventionnel : `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`, `test: ...`, `chore: ...`.
   - Zéro émoji dans les messages de commit.
3. **Revue et Intégration** :
   - Validation de l'ensemble des tests automatisés et des audits de sécurité en local avant ouverture de pull request.
   - Fusion systématique sur `developp`.

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
