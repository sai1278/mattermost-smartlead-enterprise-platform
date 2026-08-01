# Deployment Procedures

## Local Docker deployment

Use the Makefile targets for normal lifecycle management:

```bash
make up
make monitoring-up
```

The bootstrap and lifecycle scripts enforce:

- explicit `.env` handling
- health-based startup ordering
- idempotent Compose entrypoints
- a clean separation between core services and monitoring services

## Kubernetes preparation

The repository includes a Kustomize base and overlay structure for parser job execution:

- `infrastructure/kubernetes/base/`
- `infrastructure/kubernetes/overlays/local/`
- `infrastructure/kubernetes/overlays/staging/`

This does not replace the official Mattermost Helm chart or operator. Instead,
it shows how the migration worker can be promoted into cluster-native batch
execution while Mattermost itself is managed on a supported platform surface.

## Attachment Lifecycle & Package Validation

- **Download Staging**: Attachments extracted during Teams export transformation are staged at `<output_dir>/attachments/`.
- **Pre-Import Validation**: Before importing into Mattermost, `validate-import.sh` runs mandatory attachment validation to scan every post record in the JSONL payload, verifying that every referenced attachment file exists and is non-empty (`size > 0`). If any attachment is missing, validation fails fast before modifying Mattermost database state.
- **Container Staging**: When applying bulk import, both `import_data.jsonl` AND the `attachments/` directory are copied to `/tmp/` in the Mattermost container with correct `2000:2000` user permissions.

