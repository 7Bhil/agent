# État Courant de Session & Tâches Actives

État présent uniquement (40 lignes maximum). L'historique est dans `git log`.

---

## 1. Tâche Actuelle
- **Objectif** : Fusion du conseil d'arbitrage d'architecture et du cadrage contradictoire sur developp.
- **Branche Active** : `developp`.

## 2. Actions Complétées
- [x] Confinement de `decision-council.md` sous `.agent/guides/`.
- [x] Intégration du conseil d'arbitrage et du mot-clé ("passe au conseil") dans `core/RULES.md` et `.agent/guides/decision-council.md`.
- [x] Ajout du script garde-fou `scripts/check-decision-gate.py` et intégration dans `scripts/test-kit.sh`.
- [x] Numérotation séquentielle des ADR (0005 pour le conseil d'arbitrage, 0006 pour le cadrage contradictoire).
- [x] Synchronisation déterministe des adapters via `scripts/build-adapters.py`.

## 3. Prochaine Étape
- Validation finale du banc de tests `./scripts/test-kit.sh` et finalisation du commit de merge.
