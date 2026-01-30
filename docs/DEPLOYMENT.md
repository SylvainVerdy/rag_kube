# Guide de Déploiement

## Prérequis

- Docker et Docker Compose
- Kubernetes cluster (minikube, kind, ou cloud)
- kubectl configuré
- Accès à un registry Docker (GitLab Registry, Docker Hub, etc.)

## Déploiement Local avec Docker Compose

### 1. Configuration

```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env avec vos clés API
nano .env
```

### 2. Lancer les services

```bash
docker-compose up -d
```

### 3. Vérifier les services

```bash
# Vérifier les conteneurs
docker-compose ps

# Vérifier les logs
docker-compose logs -f rag-api
```

### 4. Accéder aux services

- API: http://localhost:8000
- MLflow: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)

## Déploiement Kubernetes

### 1. Préparer les secrets

```bash
# Créer le secret depuis l'exemple
cp k8s/secret.yaml.example k8s/secret.yaml

# Éditer avec vos vraies clés
nano k8s/secret.yaml

# Appliquer le secret
kubectl apply -f k8s/secret.yaml
```

### 2. Appliquer les manifests

```bash
# Créer le namespace
kubectl apply -f k8s/namespace.yaml

# Appliquer les ConfigMaps
kubectl apply -f k8s/configmap.yaml

# Appliquer les PVCs
kubectl apply -f k8s/pvc.yaml

# Appliquer les deployments
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/mlflow-deployment.yaml

# Appliquer les services
kubectl apply -f k8s/service.yaml

# Appliquer l'ingress (optionnel)
kubectl apply -f k8s/ingress.yaml
```

### 3. Vérifier le déploiement

```bash
# Vérifier les pods
kubectl get pods -n rag-system

# Vérifier les services
kubectl get svc -n rag-system

# Vérifier les logs
kubectl logs -f deployment/rag-api -n rag-system
```

### 4. Port-forward pour accès local

```bash
# API
kubectl port-forward svc/rag-api-service 8000:80 -n rag-system

# MLflow
kubectl port-forward svc/mlflow-service 5000:5000 -n rag-system
```

## Déploiement avec Kustomize

```bash
# Utiliser kustomize pour appliquer tous les manifests
kubectl apply -k k8s/
```

## CI/CD avec GitLab

### 1. Configurer les variables CI/CD

Dans GitLab: Settings > CI/CD > Variables

- `KUBE_CONTEXT_STAGING`
- `KUBE_CONTEXT_PRODUCTION`
- `GITOPS_REPO_URL` (optionnel)
- `GITOPS_TOKEN` (optionnel)

### 2. Pipeline automatique

Le pipeline GitLab CI/CD s'exécute automatiquement sur:
- **Merge Requests**: Tests et linting
- **develop**: Build et déploiement staging
- **main**: Build et déploiement production (manuel)

### 3. GitOps (ArgoCD/Flux)

Pour utiliser GitOps:

1. Créer un repository GitOps séparé
2. Configurer ArgoCD ou Flux pour surveiller ce repository
3. Le job `gitops:update` mettra à jour automatiquement les manifests

## Mise à jour

### Mise à jour de l'image

```bash
# Build et push de la nouvelle image
docker build -t rag-api:new-version .
docker push rag-api:new-version

# Mise à jour du deployment
kubectl set image deployment/rag-api rag-api=rag-api:new-version -n rag-system

# Vérifier le rollout
kubectl rollout status deployment/rag-api -n rag-system
```

### Rollback

```bash
# Voir l'historique
kubectl rollout history deployment/rag-api -n rag-system

# Rollback vers la version précédente
kubectl rollout undo deployment/rag-api -n rag-system
```

## Monitoring

### Accéder à Prometheus

```bash
kubectl port-forward svc/prometheus 9090:9090 -n monitoring
```

### Accéder à Grafana

```bash
kubectl port-forward svc/grafana 3001:3000 -n monitoring
```

### Métriques disponibles

- `rag_queries_total`: Nombre total de requêtes
- `rag_query_duration_seconds`: Durée des requêtes
- `rag_retrieval_docs_count`: Nombre de documents récupérés
- `rag_answer_length`: Longueur des réponses
- `rag_active_queries`: Requêtes actives
- `rag_vector_store_size`: Taille du vector store

## Troubleshooting

### Pods en CrashLoopBackOff

```bash
# Vérifier les logs
kubectl logs <pod-name> -n rag-system

# Vérifier les événements
kubectl describe pod <pod-name> -n rag-system
```

### Problèmes de connexion

```bash
# Vérifier les services
kubectl get svc -n rag-system

# Vérifier les endpoints
kubectl get endpoints -n rag-system
```

### Problèmes de stockage

```bash
# Vérifier les PVCs
kubectl get pvc -n rag-system

# Vérifier les PVs
kubectl get pv
```



