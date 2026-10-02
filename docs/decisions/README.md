# Format Standard des Décisions d'Architecture (ADR)

Les Architecture Decision Records (ADR) consignent les décisions architecturales et techniques structurantes du projet. Chaque décision doit faire l'objet d'un fichier Markdown numéroté dans ce répertoire (`0001-titre-court.md`).

---

## Quand Créer un ADR ?
Un ADR doit être rédigé **uniquement** pour des arbitrages techniques durables et structurants :
1. **Changement de paradigme technique** : Choix ou remplacement d'un framework, d'un ORM, d'un moteur de base de données.
2. **Stratégie de sécurité ou d'authentification** : Adoption d'un protocole d'authentification (OAuth2, JWT asymétrique, WebAuthn), politique de gestion des clés.
3. **Architecture des données & flux** : Implémentation d'un grand livre à double entrée, partitionnement, bus de messages asynchrones.
4. **Gouvernance et intégration** : Refonte de la stratégie de branches, standardisation d'outils de CI/CD bloquants.

## Quand NE PAS Créer un ADR ?
Ne pas créer d'ADR pour :
- Une correction de bug localisée ou un patch de sécurité ponctuel.
- L'ajout d'une nouvelle route ou d'un composant respectant l'architecture existante.
- Des ajustements de mise en page CSS ou de libellés d'interface.
- Des détails temporaires de session (qui vont dans `.agent/memory/current-state.md`).

---

## Modèle de Fichier ADR

```markdown
# [Numéro] - [Titre de la Décision]

- **Date** : AAAA-MM-JJ
- **Statut** : Proposé | Accepté | Remplacé par [ADR-XXXX] | Rejeté
- **Décideurs** : [Noms ou rôles des contributeurs concernés]

## Contexte et Problématique
Expliquer clairement le contexte métier ou technique, les contraintes rencontrées et la problématique à résoudre.

## Options Envisagées
1. **Option A** : Description, avantages, inconvénients.
2. **Option B** : Description, avantages, inconvénients.

## Décision Retenue
Détailler la solution choisie, la justification de ce choix et le principe de mise en œuvre.

## Conséquences et Impacts
- **Positives** : Gains de performance, découplage, maintenabilité, standardisation.
- **Négatives / Compromis** : Dette technique assumée, complexité temporaire, montée en compétences requise.
```
