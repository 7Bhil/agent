# 0001 - Adoption du Format ADR et Découplage de la Mémoire d'Équipe

- **Date** : 2026-10-02
- **Statut** : Accepté
- **Décideurs** : Équipe d'Ingénierie Senior

## Contexte et Problématique
Initialement, l'intégralité du contexte, de l'historique et des décisions architecturales était centralisée dans un fichier unique `BRAIN.md`.

Dans un contexte de travail collaboratif ou multi-agents :
1. Un fichier unique accumule les conflits de fusion (merge conflicts) lors des revues concurrentes.
2. Le fichier grossit indéfiniment, augmentant la consommation de contexte à chaque prompt sans distinction entre mémoire opérationnelle immédiate et décisions de fond immuables.

## Options Envisagées
1. **Conserver tout dans `BRAIN.md`** : Simple mais insoutenable dès que plusieurs développeurs ou agents interviennent simultanément.
2. **Découpler `BRAIN.md` et adopter les ADR standardisés (`docs/decisions/XXXX-*.md`)** :
   - `BRAIN.md` conserve la mémoire courte, le statut courant, le workflow Git et les préférences actives.
   - Les choix structurants sont consignés dans des fichiers immuables et numérotés, évitant les conflits de merge.

## Décision Retenue
Nous adoptons le standard des Architecture Decision Records (ADR) dans le répertoire `docs/decisions/`.
- Chaque décision majeure (choix d'ORM, stratégie d'authentification, refonte d'API) est documentée dans un ADR dédié.
- `BRAIN.md` reste synthétique et sert d'index et de boussole opérationnelle pour les sessions actives.

## Conséquences et Impacts
- **Positives** : Historique inaltérable, zéro conflit de fusion sur les décisions passées, meilleure lisibilité lors de l'onboarding de nouveaux ingénieurs.
- **Compromis** : Nécessite la création systématique d'un fichier Markdown pour chaque arbitrage architectural structurant.
