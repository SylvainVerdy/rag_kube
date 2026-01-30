# Interface Web pour le Système RAG

Il existe deux façons d'accéder à l'interface web :

## Option 1 : Interface HTML (Simple)

### Démarrage

1. Démarrer l'API sur le port 8001 :
```powershell
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8001
```

2. Ouvrir votre navigateur sur :
```
http://localhost:8001
```

L'interface web s'affichera automatiquement !

### Fonctionnalités

- ✅ Interface moderne et responsive
- ✅ Historique de conversation
- ✅ Affichage des sources utilisées
- ✅ Design élégant avec animations

## Option 2 : Interface Streamlit (Recommandée)

### Installation

```powershell
pip install streamlit
```

### Démarrage

```powershell
streamlit run scripts/web_interface_streamlit.py
```

L'interface s'ouvrira automatiquement dans votre navigateur (généralement sur http://localhost:8501)

### Fonctionnalités

- ✅ Interface moderne avec Streamlit
- ✅ Historique de conversation persistant
- ✅ Affichage des sources avec expander
- ✅ Sidebar avec informations système
- ✅ Bouton pour effacer l'historique

## Comparaison

| Fonctionnalité | HTML | Streamlit |
|---------------|------|-----------|
| Installation | Aucune | `pip install streamlit` |
| Démarrage | Via API | Commande séparée |
| Historique | Oui | Oui |
| Sources | Oui | Oui (avec expander) |
| Design | Moderne | Moderne |
| Personnalisation | Facile (HTML/CSS) | Via Streamlit |

## Recommandation

- **Pour un usage simple** : Utilisez l'interface HTML (Option 1)
- **Pour plus de fonctionnalités** : Utilisez Streamlit (Option 2)

## Dépannage

### L'interface ne s'affiche pas

1. Vérifiez que l'API est bien démarrée :
```powershell
curl http://localhost:8001/health
```

2. Vérifiez que le fichier `static/index.html` existe

3. Vérifiez les logs de l'API pour les erreurs

### Erreur CORS

Si vous voyez des erreurs CORS, assurez-vous que le CORS middleware est bien configuré dans `src/api/main.py`

