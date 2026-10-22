# ADR 0005 : Intégration du Cadrage Contradictoire (Grill-Me) dans la Phase de Conception

- **Statut** : Accepté
- **Date** : 2026-10-22
- **Auteur** : 7Bhil / Antigravity

---

## 1. Contexte

Les agents d'intelligence artificielle ont tendance à amorcer l'écriture de code immédiatement après une consigne utilisateur, même lorsque celle-ci comporte des zones d'ombre, des cas d'erreur non spécifiés ou des choix architecturaux implicites. Cette approche induit des allers-retours coûteux en contexte et produit du code inadapté.

L'étude des pratiques de cadrage agentique (notamment le workflow `grill-me` / `grill-with-docs` de Matt Pocock) montre qu'une phase d'interview contradictoire systématique en amont permet d'éliminer le flou avant toute modification de fichier.

## 2. Décision

1. **Intégration dans la Phase 2 de `core/RULES.md`** :
   - Exiger formellement un cadrage contradictoire préalable sur tout sujet complexe ou ambigu avant d'écrire du code.
2. **Formalisation dans `.agent/checklists/01-architecture-et-conception.md`** :
   - Ajout d'une section dédiée (Phase 0 : Protocole de Cadrage Contradictoire).
   - Règles d'interview : 1 à 3 questions ciblées par échange, définition stricte du hors-périmètre (*out of scope*), validation du modèle de données et alignement explicite.
   - Enregistrement immédiat d'un ADR en cas de décision structurante.
3. **Maintien de la frugalité** :
   - Aucune dépendance externe ni outil tiers requis : le protocole est purement méthodologique et s'exécute nativement dans le flux conversationnel.

## 3. Conséquences

- **Positives** :
  - Élimination des réécritures dues aux malentendus de spécification.
  - Formalisation immédiate des cas limites (*edge cases*) et du périmètre d'exclusion.
  - Traçabilité immédiate des arbitrages techniques dans `docs/decisions/`.
- **Négatives / Vigilance** :
  - Nécessite de doser le questionnement pour ne pas bloquer les tâches triviales ou univoques (proportionnalité au besoin).
