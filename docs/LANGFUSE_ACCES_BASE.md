# Accéder à la base des comptes Langfuse (localhost)

La base des comptes utilisateurs Langfuse est dans **PostgreSQL**, qui tourne dans le projet Docker Langfuse. Vous pouvez y accéder en ligne de commande ou avec un client graphique.

---

## Prérequis

- Langfuse doit être **démarré** (Docker) depuis son projet, ex. :  
  `C:\Users\sylva\Documents\projet_perso\langfuse`  
  `docker compose up -d`

---

## 1. En ligne de commande (psql via Docker)

Depuis le dossier du projet **Langfuse** (pas rag_kube) :

```powershell
cd C:\Users\sylva\Documents\projet_perso\langfuse
docker compose exec postgres psql -U postgres -d langfuse
```

**Si vous avez l’erreur « database "langfuse" does not exist »** : le nom de la base peut être différent. Listez les bases :

```powershell
docker compose exec postgres psql -U postgres -l
```

Repérez le nom de la base (colonne **Name**) puis connectez-vous avec ce nom :

```powershell
docker compose exec postgres psql -U postgres -d NOM_DE_LA_BASE
```

Vous pouvez aussi vérifier dans le `.env` ou `docker-compose.yml` du projet Langfuse la variable `POSTGRES_DB` ou le nom de base dans `DATABASE_URL`.

Vous êtes alors connecté à la base Langfuse. Exemples de requêtes utiles :

```sql
-- Lister les utilisateurs (comptes)
SELECT id, email, name, "emailVerified", "createdAt" FROM users;

-- Voir les organisations et membres
SELECT * FROM organization_memberships;

-- Libérer un email pour se ré-inscrire (remplacer par l'email réel)
-- UPDATE users SET email = 'old_' || email WHERE email = 'votre@email.com';

-- Quitter psql
\q
```

**Remarque :** Si la base ne s’appelle pas `langfuse`, listez les bases avec :  
`docker compose exec postgres psql -U postgres -l`  
puis utilisez le bon nom à la place de `langfuse`.

---

## 2. Avec un client graphique (pgAdmin, DBeaver, etc.)

PostgreSQL est exposé sur **localhost:5432**. Vous pouvez vous connecter depuis votre machine avec :

| Paramètre   | Valeur type      |
|------------|------------------|
| **Hôte**  | `localhost`      |
| **Port**  | `5432`           |
| **Base**  | `postgres` (si `\l` ne montre que postgres/template0/template1, les données Langfuse sont dans `postgres`) |
| **Utilisateur** | `postgres`  |
| **Mot de passe** | À récupérer dans le projet Langfuse |

### Où trouver le mot de passe

Dans le projet Langfuse :

1. Ouvrez le **docker-compose.yml** ou le fichier **.env** utilisé par Docker.
2. Cherchez une variable du type :  
   `POSTGRES_PASSWORD` ou `DATABASE_URL` (le mot de passe peut être dans l’URL).

Exemple dans un `.env` Langfuse :

```env
POSTGRES_PASSWORD=changeme
```

Une fois le mot de passe trouvé, créez une nouvelle connexion dans votre client (pgAdmin, DBeaver, etc.) avec les paramètres ci-dessus.

### Tables utiles pour les comptes

- **`users`** : comptes utilisateurs (email, nom, mot de passe hashé, etc.)
- **`organization_memberships`** : lien utilisateurs ↔ organisations
- **`projects`** : projets (et clés API associées dans l’interface Langfuse)

---

## Résumé

| Méthode        | Où lancer la commande | Connexion                          |
|----------------|------------------------|-------------------------------------|
| **psql (Docker)** | Dossier **langfuse**   | `docker compose exec postgres psql -U postgres -d langfuse` |
| **Client graphique** | Depuis votre PC        | `localhost:5432`, user `postgres`, base `postgres` (ou le nom listé par `-l`), mot de passe dans le projet Langfuse |

Pour tout changement direct en base (ex. libérer un email), privilégier une sauvegarde ou un test sur une copie si les données sont importantes.
