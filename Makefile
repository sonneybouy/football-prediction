.PHONY: help install dev test clean build deploy

help: ## Show this help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Run development server
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

test: ## Run tests
	pytest tests/ -v --cov=app --cov-report=html

clean: ## Clean cache and temp files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .coverage htmlcov/ .pytest_cache/

lint: ## Run code formatting and linting
	black app/
	isort app/
	flake8 app/

build: ## Build Docker image
	docker build -t football-prediction:latest .

compose-up: ## Start with docker-compose
	docker-compose up -d

compose-down: ## Stop docker-compose
	docker-compose down

k8s-deploy: ## Deploy to Kubernetes
	kubectl apply -f k8s/

k8s-delete: ## Delete from Kubernetes
	kubectl delete -f k8s/

logs: ## View application logs
	kubectl logs -f deployment/football-prediction-app -n football-prediction

status: ## Check deployment status
	kubectl get pods -n football-prediction

port-forward: ## Forward local port to k8s service
	kubectl port-forward svc/football-prediction-service 8000:80 -n football-prediction

shell: ## Get shell in running container
	kubectl exec -it deployment/football-prediction-app -n football-prediction -- /bin/bash