# Incident Response & Operations Runbook

## Alert Escalation Procedures

### 1. ServiceLatencySLOBreach (p95 > 200ms)
- **Symptom:** API endpoints exceeding 200ms response latency threshold.
- **Action:** Check Grafana panel `Latency Percentiles`. Scale deployment replicas via `kubectl scale deployment <app-name> --replicas=5 -n tmmp-platform`.

### 2. CircuitBreakerTripped
- **Symptom:** Downstream backend (Smartlead, Flowable, or ClickHouse) unreachable.
- **Action:** Check downstream backend health endpoints. The circuit breaker will automatically transition to `HALF_OPEN` and self-heal once backend recovers.
