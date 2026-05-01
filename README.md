# 📚 Catalogue de Livres

> Application web Django pour gérer et consulter un catalogue de livres — industrialisée avec une chaîne DevOps complète.

[![CI Pipeline](https://github.com/Ghalia789/Catalogue_livres/actions/workflows/ci.yml/badge.svg)](https://github.com/Ghalia789/Catalogue_livres/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-4.x-green)
![Docker](https://img.shields.io/badge/Docker-ready-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-Minikube-326CE5)
![ArgoCD](https://img.shields.io/badge/GitOps-ArgoCD-orange)

---

## 🗂️ Table des matières

- [Description](#-description)
- [Architecture DevOps](#-architecture-devops)
- [Stack technique](#-stack-technique)
- [Lancer le projet localement](#-lancer-le-projet-localement)
- [Lancer avec Docker](#-lancer-avec-docker)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Déploiement Kubernetes](#-déploiement-kubernetes)
- [Monitoring](#-monitoring)
- [Structure du projet](#-structure-du-projet)

---

## 📖 Description

Le **Catalogue de Livres** est une application web permettant :

- 📋 Consulter la liste complète des livres
- ➕ Ajouter, modifier et supprimer des livres (CRUD complet)
- 🔍 Rechercher et filtrer par titre, auteur ou genre
- ⭐ Laisser des avis et des notes
- 👤 Gérer son profil utilisateur
- 🔐 Authentification (inscription / connexion / rôles Admin & Utilisateur)

---

## 🏗️ Architecture DevOps

```
Code Push → GitHub Actions CI → SonarQube + Trivy → Docker Hub
                                                          ↓
                                              ArgoCD détecte le changement
                                                          ↓
                                         Kubernetes (Minikube) déploie auto
                                                          ↓
                                         Prometheus collecte les métriques
                                                          ↓
                                           Grafana affiche les dashboards
```

| Phase | Outil |
|-------|-------|
| Plan Agile | GitHub Projects (Kanban) |
| Versioning | Git / GitHub |
| Lint & Qualité | flake8, SonarCloud |
| Tests | Django TestCase |
| Build & Push | Docker, Docker Hub |
| Sécurité | Trivy, Bandit, GitHub Secrets |
| CD GitOps | ArgoCD + Kubernetes (Minikube) |
| Monitoring | Prometheus + Grafana |

---

## 🛠️ Stack technique

| Composant | Technologie |
|-----------|-------------|
| Backend | Python 3.11 / Django |
| Frontend | Bootstrap 5 |
| Base de données | SQLite |
| Conteneurisation | Docker |
| Orchestration | Kubernetes (Minikube) |
| GitOps | ArgoCD |
| CI/CD | GitHub Actions |
| Qualité de code | SonarCloud, flake8 |
| Sécurité | Trivy, Bandit |
| Monitoring | Prometheus + Grafana |

---

## 🚀 Lancer le projet localement

### Prérequis
- Python 3.11+
- pip

### Installation

```bash
# 1. Cloner le repo
git clone https://github.com/Ghalia789/Catalogue_livres.git
cd Catalogue_livres

# 2. Créer et activer l'environnement virtuel
python -m venv .venv
# Windows :
.venv\Scripts\activate
# Linux/Mac :
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Appliquer les migrations
python manage.py migrate

# 5. Créer un superuser (accès admin)
python manage.py createsuperuser

# 6. Lancer le serveur
python manage.py runserver
```

Accéder à l'application : http://localhost:8000
Interface admin : http://localhost:8000/admin

---

## 🐳 Lancer avec Docker

```bash
# Build de l'image
docker build -t catalogue-livres:latest .

# Lancer le conteneur
docker run -p 8000:8000 catalogue-livres:latest
```

Accéder à l'application : http://localhost:8000

---

## ⚙️ CI/CD Pipeline

Le pipeline GitHub Actions se déclenche automatiquement à chaque push sur `main` ou `dev`.

### Étapes du pipeline

```
Lint & Code Quality → Run Tests → SonarQube Analysis → Security Scan → Build Docker Image → Push Docker Image
```

| Étape | Outil | Description |
|-------|-------|-------------|
| Lint | flake8 | Vérifie le style du code Python |
| Tests | Django TestCase | Exécute les tests unitaires |
| Qualité | SonarCloud | Analyse la qualité et les bugs |
| Sécurité code | Bandit | Détecte les failles dans le code Python |
| Sécurité deps | Safety | Vérifie les CVE dans les dépendances |
| Sécurité image | Trivy | Scan l'image Docker avant déploiement |
| Build | Docker | Construit l'image Docker |
| Push | Docker Hub | Publie l'image sur `farah089/catalogue-livres` |

### Secrets GitHub requis

| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Nom d'utilisateur Docker Hub |
| `DOCKERHUB_PASSWORD` | Token d'accès Docker Hub |
| `SONAR_TOKEN` | Token SonarCloud |
| `SONAR_HOST_URL` | URL SonarCloud |

---

## ☸️ Déploiement Kubernetes

### Prérequis
- Minikube
- kubectl
- ArgoCD installé

### Démarrer l'environnement

```bash
# Démarrer Minikube
minikube start

# Appliquer les manifests manuellement (setup initial uniquement)
kubectl apply -f k8s/

# Vérifier les pods
kubectl get pods -n catalogue-livres

# Accéder à l'application
minikube service catalogue-livres -n catalogue-livres
```

### GitOps avec ArgoCD

ArgoCD surveille le dossier `k8s/` du repo Git et synchronise automatiquement tout changement. **Aucune commande manuelle n'est nécessaire après le setup initial.**

```bash
# Exposer l'UI ArgoCD
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Accéder à ArgoCD : https://localhost:8080

---

## 📊 Monitoring

### Prometheus + Grafana via Helm

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace

# Accéder à Grafana
kubectl port-forward svc/monitoring-grafana -n monitoring 3000:80
```

Accéder à Grafana : http://localhost:3000

Le dashboard **"Catalogue Livres Monitoring"** affiche :
- Status des pods (`kube_pod_status_ready`)
- CPU Usage
- Memory Usage
- Nombre de pods en cours d'exécution

---

## 📁 Structure du projet

```
Catalogue_livres/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline CI/CD complet
├── catalogue_livre/            # Settings Django
├── diagrams/                   # Diagrammes UML
├── k8s/                        # Manifests Kubernetes
│   ├── namespace.yaml
│   ├── deployment.yaml
│   └── service.yaml
├── livres/                     # Application principale
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
├── templates/                  # Templates HTML
├── static/                     # Fichiers statiques
├── .flake8                     # Configuration lint
├── Dockerfile                  # Image Docker
├── manage.py
├── requirements.txt
├── sonar-project.properties    # Configuration SonarCloud
└── README.md
```

---
