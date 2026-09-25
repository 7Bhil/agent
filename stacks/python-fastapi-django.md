# 🐍 Règles Senior : Python, FastAPI & Django

---

## 1. Typage & Validation Stricte
- **Type Annotations obligatoires** : Utiliser `mypy` en mode strict. Pas de variables sans annotation de type sur les fonctions publiques.
- **Pydantic V2 / Django Forms** : Validation stricte des données d'entrée. Utiliser `model_config = ConfigDict(extra='forbid')` pour bannir le mass assignment.

---

## 2. Architecture & Performance
- **FastAPI** : Ne pas bloquer l'Event Loop avec des fonctions synchrones lentes. Déclarer `async def` uniquement si des opérations I/O asynchrones (`await`) sont utilisées ; sinon, déclarer `def` pour que FastAPI l'exécute dans un thread pool dédié.
- **Django ORM** : Prévenir le piège critique du `N+1 queries` en utilisant systématiquement `select_related()` (clés étrangères) et `prefetch_related()` (relations M2M et inverses).
