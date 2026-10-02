# 0002 - Découplage du Core Universel, des Presets Personnels et Modularité Mémoire

- **Date** : 2026-10-02
- **Statut** : Accepté
- **Décideurs** : Équipe d'Ingénierie Senior

## Contexte et Problématique
Initialement, le kit mélangeait dans ses instructions fondamentales (`AGENTS.md`, `GEMINI.md`, etc.) les règles universelles d'ingénierie logicielle (OWASP, typage strict, tests de caractérisation) et les préférences subjectives propres à 7Bhil (langue des commits exclusivement en français, branche `developp`, zéro émoji en dur).

Parallèlement, `BRAIN.md` centralisait l'index, la mémoire contextuelle, les règles et le journal des versions SemVer (plus de 23 Ko), provoquant :
1. Une saturation prématurée de la fenêtre de contexte des agents.
2. Des risques élevés de conflits de merge en environnement collaboratif.
3. L'impossibilité pour un tiers d'utiliser le Core sans adopter de force les préférences de 7Bhil.

## Options Envisagées
1. **Conserver la centralisation dans `BRAIN.md` et les fichiers racine** : Simple à maintenir manuellement, mais non portable et lourd en tokens.
2. **Découpler formellement Core, Presets et Mémoire** :
   - Un socle universel immuable d'ingénierie logicielle (`core/RULES.md`).
   - Des presets configurables par utilisateur/organisation (`presets/`).
   - Une mémoire modulaire distribuée dans `.agent/memory/` (`project.md`, `user.md`, `constraints.md`, `current-state.md`).
   - `BRAIN.md` réduit à un rôle d'index d'orientation opérationnel léger.

## Décision Retenue
Nous adoptons la stratégie de découplage complet :
- `core/RULES.md` contient 100 % des invariants d'ingénierie senior (exploration, tests, sécurité, clean code).
- `presets/7bhil.md` héberge les conventions spécifiques de l'auteur (français, `developp`, style sobre).
- `.agent/config.yml` permet à tout nouvel utilisateur de surcharger les conventions sans modifier le Core.
- `.agent/memory/` sépare le contexte technique du projet, les préférences utilisateur, les contraintes et l'état de session.

## Conséquences et Impacts
- **Positives** : Portabilité totale du kit sur n'importe quel projet d'entreprise, économie majeure de tokens (seuls les fichiers pertinents sont injectés), modularité claire.
- **Compromis** : Nécessite un script d'adaptation déterministe pour générer les fichiers cibles des assistants (`AGENTS.md`, `CLAUDE.md`, etc.) à partir du Core.
