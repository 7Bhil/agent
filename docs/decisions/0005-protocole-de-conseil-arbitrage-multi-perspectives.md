# 0004 - Protocole de Conseil d'Arbitrage Multi-Perspectives et Garde-Fou Déterministe

- **Date** : 2026-10-20
- **Statut** : Accepté
- **Décideurs** : 7Bhil

## Contexte et Problématique
La Phase 2 du Core impose un arbitrage architectural et la consignation d'un ADR dans `docs/decisions/` lors de choix structurants. Toutefois :
1. Aucun protocole précis n'encadrait la délibération avant la prise de décision.
2. L'évaluation de l'importance d'un choix était subjective, induisant des risques de biais de complaisance du modèle ou d'oublis de cas critiques.
3. Aucun mécanisme déterministe ne bloquait l'omission d'un ADR lors de modifications sensibles (schémas, sécurité, dépendances).

## Options Envisagées
1. **Adoption brute du format externe LLM Council** : Nécessite 11 sous-agents parallèles à chaque question, coûteux en tokens et inadapté au flux d'ingénierie logicielle sobre.
2. **Protocole adapté aux exigences d'ingénierie Senior avec garde-fou déterministe** :
   - Définition d'un guide d'arbitrage (`guides/decision-council.md`) centré sur 5 rôles techniques d'ingénierie (Contradicteur, Principes Premiers, Expansionniste, Observateur Neutre, Exécutant).
   - Deux modes opérationnels : Rapide (séquentiel 1 agent pour décisions standard) et Complet (multi-agents pour décisions hautement critiques).
   - Déclenchement automatique via des critères objectifs (schémas, dépendances, auth/paiement, irréversibilité).
   - Script de contrôle `scripts/check-decision-gate.py` intégré en pre-commit et CI.

## Décision Retenue
Nous adoptons l'Option 2 :
- Intégration du guide d'arbitrage `guides/decision-council.md`.
- Mise à jour du contrat universel `core/RULES.md` (Phase 2).
- Ajout du script `scripts/check-decision-gate.py` vérifié par `scripts/test-kit.sh` et activé dans `scripts/setup-git-hooks.sh` et `install.sh`.

## Conséquences et Impacts
- Garantie d'un examen contradictoire systématique avant tout choix d'architecture sensible.
- Blocage strict en pre-commit si des fichiers critiques sont altérés sans trace d'ADR.
- Maintien rigoureux du budget de tokens via le mode Rapide par défaut.
