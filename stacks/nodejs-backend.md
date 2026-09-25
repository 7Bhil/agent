# 🟩 Règles Senior : Node.js, Express & NestJS Backend

> **Sources de référence** : `references/nodebestpractices`, `references/API-Security`, `references/ASVS`.

---

## 1. Architecture en Couches Strictes
- **Controller** : Valide les entrées (`req.body`, `req.params`) via Zod/DTO et passe au Service. Ne contient aucune requête SQL/ORM.
- **Service / Use Case** : Logique métier pure, sans dépendance directe à l'objet `req` ou `res` d'Express.
- **Repository / DAL** : Accès aux données avec ORM (Prisma, Drizzle, TypeORM).

---

## 2. Sécurité & Robustesse de Production
- **Sécurité** : `helmet()`, `cors()` avec whitelist d'origines, `express-rate-limit` sur l'authentification.
- **Async Errors** : En Express 4, utiliser `express-async-errors` ou des wrappers pour éviter les blocages de promesses non capturées.
- **Gestion des Connexions** : Toujours déconnecter la base de données et fermer le serveur lors d'un `SIGTERM` / `SIGINT` (*Graceful Shutdown*).
