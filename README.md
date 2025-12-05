# Istio / Helm Hands‑On – Order Service

This repository contains a small FastAPI order service and the Kubernetes/Istio plumbing around it. The focus is on how a service is packaged and operated (image, Helm, Istio, GitOps), not on building a large application.

High‑level flow:
- FastAPI order service (products, customers, orders)
- Container image published to a registry
- Helm chart deploying v1/v2 behind a single Service
- Istio for service discovery and weighted traffic between versions
- Argo CD (planned) to manage the Helm release via Git

## Repository layout

- `orders-service/` – Python order service (FastAPI + SQLAlchemy, SQLite for demo).
- `demo-backend/` – Helm chart for the backend:
  - `deployment.yaml` – `backend-v1` and `backend-v2` Deployments, using `APP_VERSION` for version identity.
  - `service.yaml` – `backend` Service, stable DNS entry for the app.
  - `destinationrule-backend.yaml` – Istio subsets (`v1`, `v2`) for traffic policies.
  - `virtualservice-backend.yaml` – in‑mesh routing and traffic split between versions.
  - `gateway-backend.yaml`, `virtualservice-backend-ingress.yaml` – Istio ingress gateway and HTTP routing for north–south traffic.
- `base/`, `istiod/` – Helm charts used to install Istio base and control plane.

Optional GitOps manifests (for Argo CD) can be added under `argocd/` and pointed at this chart.

## Application overview

The order service exposes:
- `/` – simple JSON payload including `service` name and `version` (from `APP_VERSION`), used to verify traffic shifting.
- `/products`, `/customers`, `/orders` – basic CRUD-style APIs demonstrating how the service would be used, without exposing internal implementation details here.
The service is built into a single container image and reused for both `backend-v1` and `backend-v2`; behaviour differences are driven via configuration (environment variables and routing), which is what Istio and Helm operate on.
