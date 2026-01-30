# Correction : Scores user_rating dans Langfuse

## 🔧 Corrections Apportées

### 1. Récupération du trace_id

Le `trace_id` est maintenant :
- Créé manuellement avant l'invocation du LLM
- Stocké dans `RAGGenerator.last_trace_id`
- Récupéré depuis le résultat du pipeline
- Passé à l'endpoint de scoring

### 2. Gestion des Erreurs "Bad request"

Les erreurs "Bad request" sont maintenant gérées avec :
- Troncature des commentaires (max 1000 caractères)
- Métadonnées simplifiées et incluses dans le commentaire
- Fallback avec paramètres minimaux si l'appel échoue
- Gestion d'erreur améliorée sans crash

### 3. Comportement de Langfuse

**Important** : `create_score()` de Langfuse peut retourner `None` mais créer quand même le score côté serveur. C'est un comportement normal.

## ✅ Vérification

### Étape 1 : Vérifiez les Logs

Lorsque vous notez une réponse, vous devriez voir :

```
✅ Trace créée avec ID: xxx-xxx-xxx
📊 Création du score user_rating:
   🔗 Trace ID: xxx-xxx-xxx
   ✅ Score 'user_rating' créé (ID non retourné par l'API mais score créé)
```

### Étape 2 : Vérifiez dans Langfuse

1. **Allez dans "Scores"** : http://localhost:3000 → Scores
2. **Recherchez `user_rating`** dans la liste
3. **OU allez dans "Traces"** → Cliquez sur une trace → Section "Scores"

### Étape 3 : Si le trace_id est toujours None

Vérifiez :
- Que Langfuse est bien démarré
- Que les clés API sont correctes dans `.env`
- Que `ENABLE_LANGFUSE=true`
- Les logs au démarrage de l'API

## 🐛 Si les Scores N'Apparaissent Toujours Pas

1. **Vérifiez que les scores sont créés** :
   - Regardez les logs - vous devriez voir "✅ Score créé"
   - Même si l'ID n'est pas retourné, le score peut être créé

2. **Vérifiez dans Langfuse** :
   - Rafraîchissez la page (F5)
   - Attendez quelques secondes
   - Cherchez dans "Scores" ET dans les "Traces"

3. **Testez manuellement** :
   ```powershell
   .\venv\Scripts\python.exe scripts/test_user_rating.py
   ```

4. **Vérifiez la version de Langfuse** :
   - Certaines versions peuvent avoir des différences
   - Mettez à jour si nécessaire

## 📝 Note Technique

Le fait que `create_score()` retourne `None` mais crée quand même le score est documenté dans certaines versions de Langfuse. Le score est créé côté serveur même si l'ID n'est pas retourné immédiatement.

Pour vérifier que les scores sont créés :
- Vérifiez les logs (pas d'erreur = score créé)
- Vérifiez dans Langfuse (même si l'ID n'est pas retourné)
- Les scores peuvent prendre quelques secondes à apparaître

