# 🧪 Guide de Stratégie de Test Moderne

> **Sources de référence condensées** : `references/javascript-testing-best-practices`.

Ce guide synthétise les règles fondamentales pour concevoir une suite de tests rapide, fiable, maintenable et non fragile.

---

## 1. La Pyramide Pragmatique : Tester le Comportement, Pas les Mocks

```text
       /\
      /  \      E2E (Parcours critiques uniquement - ~10%)
     /----\
    /      \    Tests d'Intégration (Cœur de la confiance - ~60%)
   /--------\   (Base de données réelle en mémoire/Docker, vraies routes HTTP)
  /          \
 /------------\ Tests Unitaires Purs (Domaine métier complexe - ~30%)
```

### La Règle d'or de la boîte noire (Black-Box Testing)
- **Tester le résultat observable**, pas les variables ou méthodes privées.
- **Ne pas tester les détails d'implémentation** : si vous renommez une méthode interne sans changer le contrat public de sortie, les tests ne doivent **pas** casser.
- **Minimiser les mocks** : Ne mocker que les frontières système externes lentes ou payantes (envoi d'e-mails, passerelles Stripe, SMS). Laisser la base de données et l'ORM tourner dans un environnement de test isolé.

---

## 2. Anatomie d'un Test Parfait : Structure AAA

Chaque test doit être divisé en 3 blocs visuels nets : **Arrange**, **Act**, **Assert**.

```typescript
describe('OrderService.createOrder', () => {
  it('should apply discount and deduct stock when cart is valid', async () => {
    // 1. Arrange (Préparation minimale)
    const initialStock = 10;
    const product = await testFactory.createProduct({ stock: initialStock, price: 100 });
    const user = await testFactory.createUser({ discountRate: 0.1 });

    // 2. Act (Action unique exécutée)
    const order = await orderService.createOrder({
      userId: user.id,
      items: [{ productId: product.id, quantity: 2 }],
    });

    // 3. Assert (Vérification des sorties et effets de bord observables)
    expect(order.totalAmount).toBe(180); // (100 * 2) - 10%
    const updatedProduct = await db.product.findUnique({ where: { id: product.id } });
    expect(updatedProduct?.stock).toBe(initialStock - 2);
  });
});
```

---

## 3. Bonnes Pratiques de Nommage et Robustesse

### 3.1 Nommage explicite selon le pattern Given-When-Then
- ❌ `it('test error', ...)`
- ❌ `it('create order works', ...)`
- ✅ `it('should return 400 with VALIDATION_ERROR when email is malformed', ...)`
- ✅ `it('should throw InsufficientStockError when quantity exceeds inventory', ...)`

### 3.2 Indépendance absolue des tests
- Chaque test doit pouvoir être exécuté seul, dans n'importe quel ordre.
- Nettoyage automatique avant chaque exécution (`beforeEach`) :
```typescript
beforeEach(async () => {
  await testDb.cleanAllTables();
});
```
