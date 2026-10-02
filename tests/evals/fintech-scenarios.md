# Banc d'Évaluation Fintech & Systèmes Transactionnels

Ce document formalise les scénarios de test critiques dédiés aux applications monétaires, aux opérations bancaires, à l'idempotence et aux passerelles Mobile Money.

---

## Scénario FIN-01 : Unités Mineures & Rejet des Nombres Flottants

### Prompt
> "Calcule le total d'un panier composé de 3 articles à 0.10 EUR et applique une remise de 0.05 EUR."

### Critères d'Évaluation
- [ ] **PASS** :
  - L'agent refuse d'effectuer `0.10 * 3 - 0.05` avec des types `number` flottants.
  - L'agent convertit immédiatement en unités mineures entières (centimes) : `10 cents * 3 - 5 cents = 25 cents`.
  - L'agent formate le résultat pour l'affichage uniquement en sortie (`0,25 EUR`).
- [ ] **FAIL** :
  - L'agent produit des calculs avec des nombres décimaux binaires exposés aux erreurs d'arrondi.

---

## Scénario FIN-02 : Grand Livre Immuable à Double Entrée (Double-Entry Ledger)

### Prompt
> "Un client effectue un transfert de 5 000 XOF de son compte A vers le compte B. Mets à jour les soldes."

### Critères d'Évaluation
- [ ] **PASS** :
  - L'agent refuse de se contenter d'un simple `UPDATE accounts SET balance = balance - 5000 WHERE id = A` et `UPDATE accounts SET balance = balance + 5000 WHERE id = B`.
  - L'agent insère une transaction comptable atomique contenant deux écritures immuables (1 débit de -5000 et 1 crédit de +5000) dont la somme arithmétique est strictement égale à 0.
  - L'agent encapsule les opérations dans un bloc transactionnel SQL avec niveau d'isolation strict.
- [ ] **FAIL** :
  - L'agent met à jour directement des colonnes sans trace d'audit ou hors transaction atomique.

---

## Scénario FIN-03 : Idempotence et Prévention des Doubles Débits

### Prompt
> "Crée la route HTTP `POST /api/transfers` pour déclencher un débit bancaire."

### Critères d'Évaluation
- [ ] **PASS** :
  - L'agent impose la présence de l'en-tête `Idempotency-Key` dans la requête entrante.
  - L'agent implémente la vérification préalable de la clé (dans Redis ou base relationnelle) pour renvoyer le résultat mémorisé en cas de requête rejouée.
  - L'agent pose un verrou distribué (mutex) pour empêcher l'exécution concurrente de deux requêtes identiques simultanées.
- [ ] **FAIL** :
  - L'agent exécute la création financière sans contrôle d'idempotence ni protection contre les doubles clics.

---

## Scénario FIN-04 : Signature HMAC Webhook Mobile Money (FedaPay / KKiaPay)

### Prompt
> "Écris le handler Express pour recevoir le webhook de notification de paiement d'un agrégateur Mobile Money."

### Critères d'Évaluation
- [ ] **PASS** :
  - L'agent calcule le condensat HMAC SHA-256 du corps brut (`raw body`) avec la clé secrète de webhook.
  - L'agent compare la signature calculée avec l'en-tête de la requête en temps constant (`crypto.timingSafeEqual`).
  - L'agent renvoie immédiatement un statut HTTP `200 OK` et déporte le traitement métier dans une file de messages asynchrone.
- [ ] **FAIL** :
  - L'agent compare les signatures avec un opérateur d'égalité standard (`===`), vulnérable aux attaques par timing.
  - L'agent effectue des opérations de traitement lourdes de 15 secondes avant de répondre au webhook.
