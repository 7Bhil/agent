# Format Standard des Décisions d'Architecture (ADR)

Les Architecture Decision Records (ADR) consignent les décisions architecturales et techniques structurantes du projet. Chaque décision doit faire l'objet d'un fichier Markdown numéroté dans ce répertoire (`0001-titre-court.md`).

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
