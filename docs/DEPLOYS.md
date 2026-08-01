# Enterprise Deployment & Operations Guide

## Local Development & Verification
```bash
# Start complete platform
docker-compose -f docker-compose.enterprise.yml up -d

# Verify all service health endpoints
curl http://localhost:8000/health # Command Handler
curl http://localhost:8001/health # Smartlead Sync
curl http://localhost:8002/health # Mattermost Bot
curl http://localhost:8003/health # Analytics Service
curl http://localhost:8004/health # Workflow Engine
```

## Kubernetes Deployment
```bash
# Apply namespace and deployment manifests
kubectl apply -f infrastructure/kubernetes/manifests/enterprise-platform.yaml

# Verify pod readiness
kubectl get pods -n tmmp-platform
```
