# Guide d'Arbitrage et Conseil Multi-Perspectives

Ce guide définit le protocole délibératif d'ingénierie logicielle pour challenger et valider toute décision architecturale avant engagement ou rédaction d'un ADR dans `docs/decisions/`.

---

## 1. Critères de Déclenchement

Le conseil d'arbitrage est déclenché selon deux modalités :

### A. Déclenchement Explicite (Directives Utilisateur)
Toute formulation équivalente à :
- `"passe au conseil"` / `"run the council"`
- `"challenge cette décision"`
- `"j'hésite entre X et Y"` / `"arbitre entre X et Y"`

### B. Déclenchement Objectif (Garde-Fous Automatiques)
Le conseil est **obligatoire** dès qu'au moins un critère suivant est satisfait :
1. **Irréversibilité technique** : Migration de schéma destructrice, refonte de persistance, changement de runtime.
2. **Nouvelle dépendance structurante** : Ajout d'un ORM, framework web, brique d'authentification ou SDK paiement.
3. **Modélisation de données** : Nouvelle entité relationnelle, altération de modèle comptable ou grand livre.
4. **Zone de sécurité sensible** : Mécanismes d'authentification, gestion des sessions, signatures HMAC, autorisation BOLA/IDOR, traitement PII/RGPD.
5. **Contrat d'API public** : Modification de contrat REST/GraphQL, formats de webhooks entrants/sortants.
6. **Périmètre transversal** : Impact simultané sur 3 modules ou couches applicatives distinctes.

> [!NOTE]
> Le conseil n'est **jamais** invoqué pour : corrections de bugs localisés, renommages, ajustements CSS/UI cosmétiques, documentation pure ou tâches déterministes à solution unique.

---

## 2. Les 5 Perspectives Délibératives

Chaque angle examine la problématique sous un prisme exclusif sans chercher le compromis à ce stade :

1. **Le Contradicteur (Downside & Robustesse)** :
   - Recherche les failles fatales, scénarios de panne réseau, timeouts, cas limites, vulnérabilités BOLA et injections.
   - Question clé : *"Qu'est-ce qui va casser en production à 3h du matin sous charge ?"*

2. **Le Penseur par Principes Premiers (First Principles & Épure)** :
   - Dépouille le problème de ses artifices de surface. Remet en question le besoin même de la fonctionnalité (YAGNI, KISS).
   - Question clé : *"Quel est le problème fondamental et pouvons-nous le résoudre sans ajouter de complexité ?"*

3. **L'Expansionniste (Évolutivité & Vision Système)** :
   - Analyse la viabilité à long terme, la réutilisabilité et l'alignement avec les futures extensions.
   - Question clé : *"Comment cette solution se comporte-t-elle si le volume ou le périmètre est multiplié par 10 ?"*

4. **L'Observateur Neutre (Clarté & Maintenabilité Externe)** :
   - Ignore l'historique implicite et évalue la lisibilité pour un ingénieur arrivant sur le projet (chesterton fence, clarté cognitive).
   - Question clé : *"Un nouvel arrivant comprendra-t-il cette architecture sans explication orale ?"*

5. **L'Exécutant Pragmatique (Faisabilité & Coût de Livraison)** :
   - Se concentre exclusivement sur l'implémentation opérationnelle : dépendances réelles, temps de migration, rollback plan et première étape concrète dès lundi matin.
   - Question clé : *"Quelle est la première PR minimale testable et comment fait-on machine arrière en cas d'échec ?"*

---

## 3. Modes d'Exécution

### Mode Rapide (Défaut : Décision Standard ou Outil Monolithique)
Un seul agent déroule séquentiellement les 5 angles d'analyse (5 à 10 lignes par perspective), suivi d'un arbitrage synthétique.

### Mode Complet (Environnements Multi-Agents & Décisions Hautement Critiques)
1. **Étape 1 (Cadrage)** : Formulation neutre du problème enrichi du contexte de `BRAIN.md` et `.agent/memory/`.
2. **Étape 2 (Délibération parallèle)** : 5 sous-agents indépendants produisent leur avis sans concertation.
3. **Étape 3 (Revue croisée anonymisée)** : Évaluation mutuelle anonyme (meilleur argument, angle mort principal, point omis).
4. **Étape 4 (Synthèse & Décision)** : Le synthétiseur dégage le consensus, documente le point de friction, rend une décision ferme et dicte la première action concrète.

---

## 4. Format de Sortie et Consignation ADR

Toute délibération débouche sur la structure standard suivante, intégrée le cas échéant dans la section dédiée de l'ADR (`docs/decisions/XXXX-*.md`) :

```markdown
### Verdict du Conseil d'Arbitrage : [Titre]

- **Points de Convergence** : [Signaux forts validés par plusieurs perspectives]
- **Tensions et Arbitrages** : [Divergences majeures et justification du choix tranché]
- **Angles Morts Traités** : [Points critiques relevés durant la revue]
- **Décision Retenue** : [Choix ferme sans ambiguïté ni conditionnel mou]
- **Première Action Immédiate** : [Une seule action concrète d'implémentation]
```
