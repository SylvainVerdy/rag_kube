# Configuration de Langfuse

## Étape 1 : Vérifier que Langfuse tourne

Assurez-vous que Langfuse est accessible sur http://localhost:3000

## Étape 2 : Obtenir vos clés API

1. Ouvrez http://localhost:3000 dans votre navigateur
2. Connectez-vous ou créez un compte
3. Allez dans **Settings** → **API Keys**
4. Créez une nouvelle clé API ou utilisez une existante
5. Copiez :
   - **Public Key** (LANGFUSE_PUBLIC_KEY)
   - **Secret Key** (LANGFUSE_SECRET_KEY)

## Étape 3 : Configurer le fichier .env

Éditez votre fichier `.env` et ajoutez/modifiez :

```env
# Langfuse Configuration
LANGFUSE_SECRET_KEY=votre_secret_key_ici
LANGFUSE_PUBLIC_KEY=votre_public_key_ici
LANGFUSE_HOST=http://localhost:3000
ENABLE_LANGFUSE=true
```

**Important** : Pour une instance locale, utilisez `http://localhost:3000` (sans https)

## Étape 4 : Redémarrer l'API

Après avoir modifié le `.env`, redémarrez l'API :

```powershell
# Arrêter l'API (Ctrl+C)
# Puis redémarrer :
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
```

## Étape 5 : Vérifier que ça fonctionne

1. Posez une question via l'interface web (http://localhost:8001)
2. Allez sur http://localhost:3000
3. Vous devriez voir les traces dans **Traces** ou **Sessions**

## Vérification

Pour vérifier que Langfuse est bien configuré, vous pouvez :

1. **Vérifier les logs de l'API** : Vous ne devriez pas voir d'erreur "Could not initialize Langfuse"
2. **Vérifier dans Langfuse** : Les traces devraient apparaître après chaque requête

## Dépannage

### Erreur "Could not initialize Langfuse"
- Vérifiez que les clés sont correctes dans `.env`
- Vérifiez que `LANGFUSE_HOST` pointe vers `http://localhost:3000`
- Vérifiez que Langfuse est bien démarré

### Pas de traces dans Langfuse
- Vérifiez que `ENABLE_LANGFUSE=true` dans `.env`
- Vérifiez que les clés API sont valides
- Vérifiez les logs de l'API pour des erreurs

### Erreur de connexion
- Vérifiez que Langfuse tourne sur le port 3000
- Vérifiez que l'URL est correcte (http://localhost:3000, pas https)

