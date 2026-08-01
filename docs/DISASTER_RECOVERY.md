# Disaster Recovery & Rollback Runbook

## ClickHouse Telemetry Backup & Restore
```bash
# Export ClickHouse table backup
clickhouse-client --query="FREEZE TABLE warmup_metrics"

# Restore from snapshot
clickhouse-client --query="ATTACH TABLE warmup_metrics FROM 'backup_snapshot'"
```

## Emergency Rollback Procedure
```bash
# Rollback Kubernetes deployment to previous revision
kubectl rollout undo deployment/tmmp-command-handler -n tmmp-platform
kubectl rollout status deployment/tmmp-command-handler -n tmmp-platform
```
