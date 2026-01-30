# Correction Rapide pour Langfuse

## Problème
Les traces n'apparaissent pas dans Langfuse sur http://localhost:3000

## Solution

### 1. Modifier le fichier `.env`

Ouvrez votre fichier `.env` et changez cette ligne :

```env
# AVANT (incorrect pour instance locale) :
LANGFUSE_HOST=https://cloud.langfuse.com

# APRÈS (correct pour instance locale) :
LANGFUSE_HOST=http://localhost:3000
```

### 2. Redémarrer l'API

**Important** : Vous devez redémarrer l'API pour que les changements du `.env` soient pris en compte.

```powershell
# 1. Arrêter l'API actuelle (Ctrl+C dans le terminal où elle tourne)

# 2. Redémarrer :
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
```

### 3. Vérifier

Lors du démarrage de l'API, vous devriez voir dans les logs :
```
✅ Langfuse initialisé - Host: http://localhost:3000
```

### 4. Tester

1. Posez une question via http://localhost:8001
2. Allez sur http://localhost:3000
3. Cliquez sur "Traces" dans le menu
4. Vous devriez voir les traces apparaître

## Si ça ne fonctionne toujours pas

Vérifiez que :
- ✅ Langfuse tourne bien sur http://localhost:3000
- ✅ Les clés API sont correctes dans `.env`
- ✅ L'API a été redémarrée après modification du `.env`
- ✅ Vous voyez le message "✅ Langfuse initialisé" au démarrage de l'API

