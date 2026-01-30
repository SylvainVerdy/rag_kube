# Comment Vérifier les Scores user_rating dans Langfuse

## 📍 Où Chercher les Scores

### Option 1 : Section "Scores" (Recommandé)

1. **Ouvrez Langfuse** : http://localhost:3000
2. **Cliquez sur "Scores"** dans le menu de gauche (icône 📊)
3. **Recherchez** `user_rating` dans la liste
4. **Filtrez** par nom de score si nécessaire

### Option 2 : Via les Traces

1. **Allez dans "Traces"** dans le menu
2. **Cliquez sur une trace récente** (celle où vous avez noté)
3. **Faites défiler** jusqu'à la section "Scores"
4. **Cherchez** le score `user_rating` dans la liste

### Option 3 : Recherche Globale

1. Utilisez la **barre de recherche** en haut de Langfuse
2. Tapez `user_rating`
3. Les résultats montreront les traces et scores correspondants

## 🔍 Vérification que les Scores sont Créés

### 1. Vérifiez les Logs de l'API

Lorsque vous notez une réponse depuis l'interface web, regardez les logs de l'API. Vous devriez voir :

```
📊 Création du score user_rating:
   trace_id: xxx-xxx-xxx
   value: 0.85
   comment: ...
   ✅ Score créé avec ID: xxx
```

### 2. Testez Manuellement

Créez un score de test :

```powershell
.\venv\Scripts\python.exe scripts/test_user_rating.py
```

### 3. Vérifiez la Console du Navigateur

1. Ouvrez la console (F12)
2. Notez une réponse depuis l'interface
3. Vérifiez qu'il n'y a pas d'erreurs
4. Vérifiez la réponse de l'API (onglet Network)

## ⚠️ Problèmes Possibles

### Les scores ne sont pas créés

**Symptômes** :
- Pas de message "✅ Score créé" dans les logs
- Erreur "Bad request" dans les logs
- Erreur dans la console du navigateur

**Solutions** :
1. Vérifiez que Langfuse est bien démarré
2. Vérifiez les clés API dans `.env`
3. Vérifiez que `ENABLE_LANGFUSE=true`
4. Redémarrez l'API après modification du `.env`

### Les scores sont créés mais non visibles

**Symptômes** :
- Message "✅ Score créé" dans les logs
- Pas d'erreur
- Mais pas visible dans Langfuse

**Solutions** :
1. **Rafraîchissez la page** Langfuse (F5)
2. **Attendez quelques secondes** - les scores peuvent prendre du temps à apparaître
3. **Vérifiez les filtres** - peut-être que les scores sont filtrés par date
4. **Vérifiez dans "Scores"** plutôt que dans "Traces"
5. **Vérifiez que vous êtes sur la bonne page** - certains scores peuvent être sur une autre page

### Le trace_id est None

**Symptômes** :
- Les scores sont créés mais non liés à une trace
- `trace_id: None` dans les logs

**Solutions** :
1. Vérifiez que Langfuse CallbackHandler est bien initialisé
2. Vérifiez les logs au démarrage de l'API
3. Vérifiez que `ENABLE_LANGFUSE=true` dans `.env`

## 📊 Format d'un Score user_rating

Un score `user_rating` devrait avoir :

- **Name** : `user_rating`
- **Value** : Valeur entre 0.0 et 1.0
- **Trace ID** : ID de la trace associée (si disponible)
- **Comment** : Commentaire + métadonnées
- **Created At** : Date et heure de création

## 🧪 Test Complet

Pour tester complètement le système :

1. **Démarrez l'API** avec les logs visibles
2. **Ouvrez l'interface web** : http://localhost:8001
3. **Posez une question**
4. **Notez la réponse** avec 👍, 👎, ou ⭐
5. **Vérifiez les logs** de l'API
6. **Allez dans Langfuse** : http://localhost:3000
7. **Cherchez le score** dans "Scores" ou dans la trace correspondante

## 💡 Astuces

- Les scores peuvent prendre **quelques secondes** à apparaître dans Langfuse
- **Rafraîchissez toujours** la page Langfuse après avoir noté
- Utilisez la **recherche** pour trouver rapidement les scores
- Les scores sont **liés aux traces** - ouvrez une trace pour voir ses scores

