# État Courant de Session & Tâches Actives

État présent uniquement (40 lignes maximum). L'historique est dans `git log`.

---

## 1. Tâche Actuelle
- **Objectif** : Réduction du coût en tokens du kit.
- **Branche Active** : `refactor/economie-tokens`.

## 2. Actions Complétées
- [x] `GEMINI.md` et `CLAUDE.md` réduits à des renvois vers `AGENTS.md` (`CLAUDE.md` via import `@AGENTS.md`). Supprime la double injection sous Antigravity (~2 600 tokens par tour).
- [x] Règle du premier réflexe proportionnée : lecture mémoire une fois par session, écriture de `current-state.md` seulement après modification de fichiers, mémoire bornée à 40 lignes.
- [x] Test de budget de contexte ajouté à `scripts/test-kit.sh` (AGENTS.md <= 10 Ko, renvois <= 600 o, current-state <= 40 lignes).

## 3. Décisions en Attente
- Conseil d'arbitrage ADR (inspiré de `aiwithremy/claude-skills-llm-council`, sans licence : réécriture obligatoire). Déclenchement : demande explicite, critères objectifs (irréversible, dépendance structurante, schéma, zone sensible, contrat public, options multiples, >= 3 modules), garde-fou par script sur le diff. Modes rapide et complet.
- Compression de `AGENTS.md` sous 4 Ko (explications déplacées dans `core/RULES.md`).

## 4. Prochaine Étape
- Validation utilisateur, merge `--no-ff` sur `developp`, puis branche `feature/conseil-arbitrage-adr`.
