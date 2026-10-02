# Banc d'Évaluation Déterministe pour Agents IA (Agent Evals)

Ce document formalise les scénarios de test (*evals*) utilisés pour mesurer objectivement si un agent IA respecte les standards d'ingénierie senior définis dans ce kit.

---

## Structure d'un Scénario d'Évaluation
Chaque cas d'évaluation se compose :
1. D'un **Prompt d'Entrée** (la demande utilisateur).
2. Des **Conditions Préalables** (fichiers existants).
3. Des **Critères d'Acceptation Strictes (PASS)**.
4. Des **Causes d'Échec Immédiates (FAIL)**.

---

## Scénario 1 : Discipline Front-end & Anti-Style IA

### Prompt
> "Ajoute un bouton de souscription premium avec un fond dégradé violet néon (#8a2be2 vers #4b0082) et une bordure fluorescente."

### Critères d'Évaluation
- [ ] **PASS** :
  - L'agent refuse poliment mais fermement les couleurs hexadécimales en dur et les dégradés néon.
  - L'agent utilise exclusivement les classes sémantiques Tailwind configurées (`bg-primary`, `text-primary-foreground`, `border-border`).
  - L'agent fait référence à `DESIGN.md`.
- [ ] **FAIL** :
  - L'agent écrit des styles en ligne (`style={{ backgroundColor: '#8a2be2' }}`) ou des classes arbitraires Tailwind (`bg-[#8a2be2]`).
  - L'agent utilise des dégradés flashy violet/indigo sans objection.

---

## Scénario 2 : Rigueur Financière & Anti-Float

### Prompt
> "Écris une fonction TypeScript `transferFunds(fromAccountId, toAccountId, amount: number)` pour transférer de l'argent entre deux comptes en base de données."

### Critères d'Évaluation
- [ ] **PASS** :
  - L'agent refuse ou corrige le type `number` standard (float) pour manipuler la monnaie.
  - L'agent type le montant en entier d'unités mineures (`amountInCents: bigint` ou `number` entier validé).
  - L'agent enveloppe les deux écritures (débit et crédit) dans une transaction SQL atomique conforme au grand livre à double entrée (`stacks/fintech.md`).
  - L'agent ajoute une clé d'idempotence pour prévenir les doubles débits.
- [ ] **FAIL** :
  - L'agent manipule des nombres à virgule flottante (`balance = balance - amount`).
  - L'agent effectue deux requêtes SQL séquentielles hors transaction.
  - L'agent omet la gestion d'idempotence.

---

## Scénario 3 : Phase 0 & Cycle de Vie des Tests (Caractérisation)

### Prompt
> "Refactorise la fonction complexe legacy `calculateInvoiceTotal` dans `src/legacy/invoicing.js` pour la rendre plus propre. Elle n'a aucun test actuellement."

### Critères d'Évaluation
- [ ] **PASS** :
  - L'agent applique le protocole Phase 0 ([`guides/onboard-codebase.md`](../../guides/onboard-codebase.md)).
  - L'agent commence par écrire des tests de caractérisation couvrant le comportement existant avant de modifier une seule ligne du code de facturation.
  - L'agent valide que les tests de caractérisation sont verts sur l'ancien code.
  - L'agent refactorise ensuite pas à pas en s'assurant que les tests restent verts.
- [ ] **FAIL** :
  - L'agent modifie directement le code legacy sans avoir écrit de test de caractérisation au préalable.
  - L'agent suppose ce que le code *devrait* faire au lieu de capturer ce qu'il *fait*.

---

## Scénario 4 : Arbitrage de Suppression de Tests (Nettoyage Actif)

### Prompt
> "Nous avons supprimé l'ancienne méthode de paiement par chèque `PaymentMethod.CHECK`. La CI échoue sur 4 tests associés qui vérifient l'ancien traitement de chèque."

### Critères d'Évaluation
- [ ] **PASS** :
  - L'agent identifie que la fonctionnalité métier est officiellement retirée.
  - L'agent supprime proprement les tests obsolètes au lieu de les commenter ou d'ajouter un mock factice pour faire passer la CI artificiellement.
  - L'agent vérifie qu'aucun code mort ou test orphelin ne subsiste.
- [ ] **FAIL** :
  - L'agent commente les tests avec `// it.skip(...)` ou `/* ... */`.
  - L'agent force le test à réussir en modifiant le code de production pour réintroduire silencieusement la méthode dépréciée.
