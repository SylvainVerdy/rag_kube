# Dépannage : Scores user_rating dans Langfuse

## 🔍 Où trouver les scores dans Langfuse

### Méthode 1 : Section "Scores"

1. Ouvrez Langfuse : http://localhost:3000
2. Cliquez sur **"Scores"** dans le menu de gauche
3. Recherchez les scores avec le nom `user_rating`
4. Utilisez le filtre pour rechercher par nom de score

### Méthode 2 : Via les Traces

1. Allez dans **"Traces"**
2. Cliquez sur une trace spécifique
3. Les scores associés à cette trace apparaissent dans la section "Scores" de la trace
4. Recherchez le score `user_rating` dans la liste

### Méthode 3 : Recherche globale

1. Utilisez la barre de recherche en haut
2. Tapez `user_rating`
3. Les résultats incluront les traces et scores correspondants

## 🐛 Problèmes courants

### Les scores n'apparaissent pas

**Vérification 1 : Les scores sont-ils créés ?**

Vérifiez les logs de l'API lorsque vous notez une réponse. Vous devriez voir :
```
📊 Création du score user_rating:
   trace_id: xxx
   value: 0.85
   ✅ Score créé avec ID: xxx
```

**Vérification 2 : Le trace_id est-il présent ?**

Si `trace_id` est `None`, les scores peuvent être créés mais non liés à une trace. Vérifiez :
- Que Langfuse est bien configuré
- Que le CallbackHandler fonctionne
- Les logs au démarrage de l'API

**Vérification 3 : Test manuel**

Testez la création d'un score manuellement :

```powershell
.\venv\Scripts\python.exe scripts/test_user_rating.py
```

### Erreur "Bad request"

Cette erreur peut apparaître si :
- Les paramètres passés à `create_score` ne sont pas corrects
- La version de Langfuse ne supporte pas certains paramètres
- Les métadonnées sont trop complexes

**Solution** : Les métadonnées sont maintenant incluses dans le commentaire au lieu d'être passées séparément.

### Le score est créé mais non visible

1. **Rafraîchissez la page** Langfuse
2. **Vérifiez les filtres** - peut-être que les scores sont filtrés
3. **Vérifiez la date** - les scores récents peuvent prendre quelques secondes à apparaître
4. **Vérifiez dans "Scores"** plutôt que dans "Traces"

## ✅ Vérification étape par étape

### 1. Vérifier que l'API reçoit la requête

Dans la console du navigateur (F12), vérifiez que la requête POST vers `/api/langfuse/score/rag` :
- Retourne un statut 200
- Contient `"success": true`
- A un message de confirmation

### 2. Vérifier les logs de l'API

Lorsque vous notez une réponse, vous devriez voir dans les logs :
```
📊 Création du score user_rating:
   trace_id: xxx
   value: 0.85
   comment: ...
   ✅ Score créé avec ID: xxx
```

### 3. Vérifier dans Langfuse

1. Allez sur http://localhost:3000
2. Cliquez sur **"Scores"** dans le menu
3. Recherchez `user_rating` dans la liste
4. Cliquez sur un score pour voir les détails

## 🔧 Solution de contournement

Si les scores ne s'affichent toujours pas, vous pouvez :

1. **Vérifier directement via l'API Langfuse** :
   - Allez dans Langfuse → Settings → API Keys
   - Utilisez l'API REST directement pour créer un score

2. **Vérifier les traces** :
   - Les scores peuvent être liés aux traces même s'ils n'apparaissent pas dans la liste globale
   - Ouvrez une trace et vérifiez la section "Scores"

3. **Vérifier la version de Langfuse** :
   - Certaines versions peuvent avoir des différences dans l'affichage des scores
   - Mettez à jour Langfuse si nécessaire

## 📝 Format attendu dans Langfuse

Un score `user_rating` devrait apparaître avec :
- **Name** : `user_rating`
- **Value** : La valeur de notation (0.0 - 1.0)
- **Trace ID** : L'ID de la trace associée
- **Comment** : Le commentaire de l'utilisateur + métadonnées
- **Created At** : Date et heure de création

