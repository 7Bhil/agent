# ADR 0008 : Intégration de la Suite de Calcul Évolutionnaire

- **Statut** : Accepté
- **Date** : 2026-11-02
- **Auteur** : 7Bhil / Antigravity

---

## 1. Contexte

Le kit Senior Agent Core s'appuie sur des règles déterministes d'ingénierie et des bancs de tests statiques.
Toutefois, deux besoins complémentaires émergeaient :
1. Éprouver la robustesse des règles et filtres (anti-slop, typage strict, sécurité des flux) face à des attaques combinatoires ou des instructions contradictoires générées dynamiquement.
2. Disposer de patrons formels et standardisés pour concevoir des algorithmes métaheuristiques déterministes et typés (TypeScript / Python) sans bibliothèques externes lourdes.
3. Permettre l'optimisation automatisée des prompts et instructions en respectant le budget strict de contexte.

## 2. Décision

1. **Moteur de Fuzzing Adverse Évolutionnaire (`scripts/fuzz-agent-evals.py`)** :
   - Algorithme génétique autonome basé sur la bibliothèque standard Python.
   - Opérateurs de mutation, croisement et sélection par tournoi générant des cas limites complexes.
   - Reproductibilité déterministe via paramètre de graine pseudo-aléatoire (`--seed`).
2. **Guide d'Ingénierie Métaheuristique (`.agent/guides/evolutionary-computation.md`)** :
   - Contrat d'ingénierie senior pour le calcul évolutionnaire : découplage génotype/phénotype, fitness pure, PRNG explicite, typage strict sans `any`.
   - Modèles d'implémentation complets en TypeScript et Python.
   - Directives pour l'optimisation multi-objectifs (front de Pareto / NSGA-II).
3. **Optimiseur de Prompts et Règles (`scripts/optimize-prompts-ea.py`)** :
   - Outil génétique d'optimisation textuelle maximisant la couverture des règles tout en minimisant la verbosité et en éradiquant le slop.
4. **Intégration au Banc de Test (`scripts/test-kit.sh`)** :
   - Validation automatisée des self-tests de la suite évolutionnaire dans le cycle d'intégrité global.

## 3. Conséquences

- **Positives** :
  - Capacité native à générer des cas de tests adverses complexes de manière automatisée.
  - Standard clair et industrialisable pour les projets clients nécessitant de l'optimisation combinatoire bio-inspirée.
  - Zéro dépendance externe ajoutée (Python standard library uniquement).
- **Vigilance** :
  - Conserver un budget d'évaluation modéré (taille de population et nombre de générations) pour maintenir l'exécution des tests en quelques secondes.
