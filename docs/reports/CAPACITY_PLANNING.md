# Mattermost ↔ Smartlead Enterprise Platform: Capacity Planning Guide

**Role:** Google Staff SRE & Principal Infrastructure Architect  
**Date:** August 1, 2026  
**Repository:** `teams-mattermost-migration`  

---

## Executive Overview

This capacity plan establishes production resource sizing, autoscaling rules, queue buffer sizing, and storage growth projections for the **Mattermost ↔ Smartlead Enterprise Platform** based on empirical benchmark data (up to 5,000 VUs / 46,000+ RPS).

---

## 1. Microservice Resource Specifications (Kubernetes Pod Sizing)

| Component | CPU Requests | CPU Limits | Memory Requests | Memory Limits | Target Replica Count (Baseline) | Max Replicas (HPA) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `apps/command-handler` | `250m` | `1000m` | `256Mi` | `512Mi` | 2 | 10 |
| `apps/smartlead-sync` | `500m` | `2000m` | `512Mi` | `1024Mi` | 3 | 15 |
| `apps/bot` | `250m` | `1000m` | `256Mi` | `512Mi` | 2 | 8 |
| `apps/analytics` | `500m` | `2000m` | `512Mi` | `2048Mi` | 3 | 20 |
| `apps/workflow-engine` | `500m` | `1500m` | `512Mi` | `1024Mi` | 2 | 10 |

---

## 2. Horizontal Pod Autoscaling (HPA) Policies

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: tmmp-analytics-hpa
  namespace: tmmp-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: tmmp-analytics
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

---

## 3. Storage & Buffer Capacity Planning

1. **Redis Telemetry Queue:**
   - Peak throughput: 50,000 events/sec.
   - Payload size per event: ~500 bytes.
   - Required Redis Memory Buffer: **4 GB minimum** for 10-minute network partition survival.

2. **ClickHouse Columnar Database Storage:**
   - Daily ingestion rate: ~1.2 GB / million events (compressed with LZ4/ZSTD).
   - Monthly projected storage per 10 million events/day: **36 GB / month**.
   - Recommended disk volume: **500 GB NVMe SSD** with automated TTL retention policies (`TTL timestamp + INTERVAL 90 DAY`).

---

## 4. Head-Room & Safety Margin Strategy

- **Head-room Formula:** `Target CPU Utilization = 60-70%`. Reserves a 30-40% surge capacity for sudden traffic spikes.
- **Failover Headroom:** N+1 redundancy across all microservice deployments. If one node or pod crashes, remaining replicas handle 100% of peak load without breaching latency SLOs.
