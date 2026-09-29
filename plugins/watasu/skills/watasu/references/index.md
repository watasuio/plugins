# Watasu handbook

This is the customer-side, zero-to-hero guide to Watasu. Read a track in order
to learn the platform, or jump from the task map. Each chapter stays narrow so
an agent can load only the context it needs.

## Application track

1. [Customer boundaries](customer-boundaries.md)
   Start with [supported surfaces](capabilities.md) and
   [setup and authentication](authentication.md) on a new account.
2. [Concepts and lifecycle](concepts-and-lifecycle.md)
3. [First deploy](first-deploy.md)
4. [Builds and buildpacks](builds-and-buildpacks.md)
5. [Dockerfiles and non-root containers](dockerfiles-and-containers.md)
6. [Configuration and secrets](config-and-secrets.md)
7. [Processes, networking, and domains](processes-networking-and-domains.md)
8. [`PORT`, health, and startup](ports-health-and-startup.md)
9. [Release commands and migrations](release-commands-and-migrations.md)
10. [Domains and private networking](domains-and-private-networking.md)
11. [RTC and TURN](rtc.md)
12. [GitHub deployments, pipelines, and review apps](github-workflows.md)
13. [`app.json`](app-json.md)
14. [Add-ons and data](addons-and-data.md)
15. [Observability](observability.md)
16. [Metrics and `METRICS_PORT`](metrics.md)
17. [CLI](cli.md)
18. [MCP](mcp.md)
19. [Teams, access, and billing](teams-access-and-billing.md)
20. [Application debugging](app-debugging.md)

## Data, access, and operations

- [PostgreSQL, connections, and followers](postgresql.md)
- [Valkey and ClickHouse](valkey-and-clickhouse.md)
- [Redpanda and object storage](streaming-and-object-storage.md)
- [Backups, downloads, restores, and promotion](backups-and-restores.md)
- [Stored logs, live output, and traces](logs-and-traces.md)
- [Authentication and credential scope](authentication.md)
- [API errors and safe retries](api-errors.md)
- [CLI/MCP capabilities and dashboard handoffs](capabilities.md)

## Sandbox track

1. [Sandbox overview](sandboxes.md)
2. [Lifecycle and API contract](sandbox-lifecycle.md)
3. [Templates and Dockerfile conversion](sandbox-templates.md)
4. [SDK selection and recipes](sdk-recipes.md)
5. [Files and `apply_diff`](sandbox-files-apply-diff.md)
6. [Commands, processes, and PTY](sandbox-processes-pty.md)
7. [Git automation](sandbox-git.md)
8. [Networking and previews](sandbox-networking.md)
9. [Pause, checkpoints, and volumes](sandbox-state-and-storage.md)
10. [Advanced SSH](sandbox-ssh.md)
11. [Code Interpreter and sandbox MCP](sandbox-mcp-code-interpreter.md)
12. [SDK capability map](sandbox-sdks.md)
13. [Sandbox debugging](sandbox-debugging.md)

## Task map

| Goal | Start here |
| --- | --- |
| Install and authenticate without platform access | [Setup](authentication.md) |
| Identify CLI/MCP limitations | [Supported surfaces](capabilities.md) |
| Resolve authentication, permission, or quota errors | [API errors](api-errors.md) |
| Deploy a repository | [First deploy](first-deploy.md) |
| Fix a Docker build or boot | [Dockerfiles](dockerfiles-and-containers.md) |
| Make a secret available during a build | [Configuration and secrets](config-and-secrets.md) |
| Fix a port or readiness failure | [`PORT` and health](ports-health-and-startup.md) |
| Run database migrations | [Release commands](release-commands-and-migrations.md) |
| Configure a domain or private TCP trust | [Domains and private networking](domains-and-private-networking.md) |
| Build an SFU/WebRTC service | [RTC and TURN](rtc.md) |
| Configure GitHub deployment | [GitHub workflows](github-workflows.md) |
| Provision review apps declaratively | [`app.json`](app-json.md) |
| Attach or restore data | [Add-ons](addons-and-data.md) |
| Capture/download a backup or validate a restore | [Backups](backups-and-restores.md) |
| Connect a database or add a read follower | [PostgreSQL](postgresql.md) |
| Connect a cache or analytical database | [Valkey and ClickHouse](valkey-and-clickhouse.md) |
| Use Kafka clients or S3 uploads | [Redpanda and object storage](streaming-and-object-storage.md) |
| Investigate a historical incident | [Logs and traces](logs-and-traces.md) |
| Allowlist outbound application addresses | [Add-ons](addons-and-data.md#outbound-ip-allowlists) |
| Fix empty metrics | [`METRICS_PORT`](metrics.md) |
| Inspect live app state safely | [MCP](mcp.md) |
| Patch sandbox files | [`apply_diff`](sandbox-files-apply-diff.md) |
| Run an interactive tool | [Processes and PTY](sandbox-processes-pty.md) |
| Expose a sandbox web server | [Networking and previews](sandbox-networking.md) |
| Reconnect to a development box | [Advanced SSH](sandbox-ssh.md) |
| Preserve or restore sandbox state | [State and storage](sandbox-state-and-storage.md) |
| Run an MCP server in a sandbox | [Sandbox MCP](sandbox-mcp-code-interpreter.md) |
| Diagnose any failure | [Application](app-debugging.md) or [sandbox](sandbox-debugging.md) |

For a single-page summary of the app lifecycle, use
[apps, deploys, and config](apps-deploys-and-config.md). For the combined
failure matrix, use [troubleshooting](troubleshooting.md).

## Sources and freshness

The [source map](source-map.md) links the public documentation and product blog;
the [coverage map](coverage.md) routes each documentation topic to this handbook.
Live product state and current docs win over this handbook for
versions, regions, plan names, limits, pricing, and flags that can change.

[Customer boundaries](customer-boundaries.md) · [Source map](source-map.md)
