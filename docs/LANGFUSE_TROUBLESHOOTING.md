# Dépannage Langfuse

## Problème : Pas de traces dans Langfuse

### Vérification 1 : Configuration du .env

Assurez-vous que votre fichier `.env` contient :

```env
LANGFUSE_SECRET_KEY=votre_secret_key
LANGFUSE_PUBLIC_KEY=votre_public_key
LANGFUSE_HOST=http://localhost:3000
ENABLE_LANGFUSE=true
```

**Important** : Pour une instance locale, utilisez `http://localhost:3000` (pas https)

### Vérification 2 : Langfuse est-il démarré ?

Vérifiez que Langfuse est accessible :
```powershell
Invoke-WebRequest -Uri "http://localhost:3000" -UseBasicParsing
```

### Vérification 3 : Clés API valides

1. Allez sur http://localhost:3000
2. Settings → API Keys
3. Vérifiez que les clés dans `.env` correspondent

### Vérification 4 : Logs de l'API

Lors du démarrage de l'API, vous devriez voir :
```
✅ Langfuse initialisé - Host: http://localhost:3000
```

Si vous voyez un warning, vérifiez les clés.

### Vérification 5 : Test manuel

Testez avec le script :
```powershell
python scripts/check_langfuse.py
```

### Vérification 6 : Redémarrer l'API

Après avoir modifié `.env`, **redémarrez toujours l'API** :
```powershell
# Arrêter (Ctrl+C)
# Puis redémarrer :
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
```

## Problèmes courants

### "Could not initialize Langfuse"
- Vérifiez que les clés sont correctes
- Vérifiez que Langfuse tourne sur le bon port
- Vérifiez l'URL (http vs https)

### Traces n'apparaissent pas immédiatement
- Langfuse peut prendre quelques secondes pour afficher les traces
- Rafraîchissez la page dans Langfuse
- Vérifiez l'onglet "Traces" ou "Sessions"

### Erreur de connexion
- Vérifiez que `LANGFUSE_HOST` est correct
- Pour local : `http://localhost:3000`
- Pour cloud : `https://cloud.langfuse.com`

