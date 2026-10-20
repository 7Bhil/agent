# 0005 - Restructuration Propre de la Racine et Standard Client-Server-Admin

- **Date** : 2026-10-20
- **Statut** : Accepté
- **Décideurs** : 7Bhil

## Contexte et Problématique
La structure initiale du kit plaçait à la racine du dépôt 26 fichiers documentaires répartis dans trois dossiers (`guides/`, `checklists/`, `stacks/`), créant un encombrement visuel inutile.
Dans les architectures réelles découpées en `client/`, `server/` et `admin/`, l'absence de contrat d'API partagé favorisait la divergence des noms d'endpoints et des payloads.

## Décision Retenue
1. **Épure de la Racine du Dépôt** :
   - Confinement de l'ensemble de la documentation opérationnelle sous le namespace masqué `.agent/` (`.agent/guides/`, `.agent/checklists/`, `.agent/stacks/`).
   - La racine reste épurée et réservée au code métier et aux fichiers de configuration indispensables (`AGENTS.md`, `BRAIN.md`, `.agent/`).
2. **Standard d'Architecture Client / Server / Admin** :
   - Introduction du pattern de **Source Unique de Vérité** dans `shared/` (`.agent/stacks/client-server-admin.md`).
   - Interdiction formelle du codage d'URLs ou de schémas en dur : utilisation obligatoire des constantes et DTOs Zod partagés via l'alias TypeScript `@shared`.
3. **Mise à Jour de l'Outillage** :
   - Adaptation déterministe de `install.sh`, `scripts/test-kit.sh` et `scripts/run-evals.py` pour valider l'intégrité de la nouvelle arborescence.

## Conséquences et Impacts
- Racine de projet propre et attrayante.
- Prévention absolue de toute désynchronisation d'endpoints entre le backend et les multiples applications frontales.
