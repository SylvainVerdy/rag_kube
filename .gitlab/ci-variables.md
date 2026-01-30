# Variables CI/CD à configurer dans GitLab

## Variables Kubernetes

- `KUBE_CONTEXT_STAGING`: Contexte kubectl pour l'environnement staging
- `KUBE_CONTEXT_PRODUCTION`: Contexte kubectl pour l'environnement production

## Variables GitOps

- `GITOPS_REPO_URL`: URL du repository GitOps (ArgoCD/Flux)
- `GITOPS_TOKEN`: Token d'accès au repository GitOps

## Variables Docker Registry

Ces variables sont automatiquement disponibles dans GitLab CI:
- `CI_REGISTRY`: Registry Docker GitLab
- `CI_REGISTRY_USER`: Utilisateur du registry
- `CI_REGISTRY_PASSWORD`: Mot de passe du registry
- `CI_REGISTRY_IMAGE`: Image Docker complète

## Configuration

1. Aller dans Settings > CI/CD > Variables
2. Ajouter les variables ci-dessus
3. Marquer les variables sensibles comme "Masked" et "Protected"



