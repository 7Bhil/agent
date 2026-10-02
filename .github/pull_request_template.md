## Description des Modifications
<!-- Décrire synthétiquement la nature du changement, le problème résolu et la solution apportée. -->

## Type de Changement
- [ ] Nouvelle fonctionnalité (`feat`)
- [ ] Correction de bug (`fix`)
- [ ] Refactorisation sans impact fonctionnel (`refactor`)
- [ ] Documentation / Spécification (`docs`)
- [ ] Tests automatisés (`test`)
- [ ] Amélioration de performance (`perf`)

## Décision d'Architecture (ADR)
<!-- Si ce changement introduit un arbitrage architectural structurant, référencer le fichier ADR correspondant dans docs/decisions/. -->
- Référence ADR : N/A ou `docs/decisions/XXXX-*.md`

## Checklist de Validation Obligatoire
- [ ] **Phase 0** : Exploration de l'existant effectuée, ligne de base des tests vérifiée.
- [ ] **Typage** : Zéro `any`, typage strict validé (`tsc --noEmit`).
- [ ] **Tests** : Nouveaux tests ajoutés couvrant le cas nominal et les cas limites.
- [ ] **Sécurité** : Validation des entrées (Zod/Valibot), contrôle BOLA/IDOR, aucun secret dans les logs.
- [ ] **Design System** : Conforme à `global.css` et `tailwind.config`, zéro couleur en dur.
- [ ] **Règles Rédactionnelles** : Zéro émoji, absence de slop IA (`audit-slop.py` validé).
- [ ] **Mémoire** : `BRAIN.md` ou ADR actualisé.
