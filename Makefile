.PHONY: help install test lint format run docker-build docker-up docker-down k8s-apply k8s-delete

help:
	@echo "Commandes disponibles:"
	@echo "  make install      - Installer les dépendances"
	@echo "  make test         - Lancer les tests"
	@echo "  make lint         - Vérifier le code"
	@echo "  make format       - Formater le code"
	@echo "  make run          - Lancer l'API localement"
	@echo "  make docker-build - Builder l'image Docker"
	@echo "  make docker-up    - Lancer avec Docker Compose"
	@echo "  make docker-down  - Arrêter Docker Compose"
	@echo "  make k8s-apply    - Appliquer les manifests K8s"
	@echo "  make k8s-delete   - Supprimer les ressources K8s"

install:
	pip install -r requirements.txt

test:
	pytest tests/ -v

lint:
	flake8 src/ --max-line-length=120
	black --check src/
	isort --check-only src/
	mypy src/ --ignore-missing-imports

format:
	black src/ tests/
	isort src/ tests/

run:
	uvicorn src.api.main:app --reload

docker-build:
	docker build -t rag-api:latest .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

k8s-apply:
	kubectl apply -f k8s/

k8s-delete:
	kubectl delete -f k8s/



