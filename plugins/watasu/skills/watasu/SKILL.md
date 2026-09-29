---
name: watasu
description: >-
  Operate Watasu from the customer side: deploy and configure apps, use the CLI
  and read-only MCP server, manage processes, domains, private networking,
  add-ons, backups, observability, GitHub deployments, pipelines, review apps,
  teams and access, and create or automate AI sandboxes through the REST API and
  official SDKs. Use whenever a task mentions Watasu, watasu.io,
  watasuhost.com, the `watasu` CLI, Watasu apps or releases, Watasu add-ons, or
  Watasu sandboxes.
---

# Watasu

Use this skill for customer-side Watasu work. Treat Watasu as a managed
platform: solve the task through its documented UI, CLI, Git, MCP, REST API, or
SDK contract. Do not turn a customer operation into an internal cluster task.
Assume the user has only their application repository, customer CLI, and MCP
connection. Never require a Watasu source checkout or infrastructure credentials.
Use [supported surfaces](references/capabilities.md) to identify gaps; if a task
needs a customer dashboard action, explain that handoff rather than inventing a
CLI or MCP operation.

The complete, cross-linked guide is the
[Watasu handbook](references/index.md). Use its ordered application or sandbox
track when the user is learning the platform; use the task map for focused work.

## Start every task this way

1. Read [customer boundaries](references/customer-boundaries.md).
2. Identify the object: team, app, build, release, process, formation, add-on,
   domain, pipeline, or sandbox.
3. For live state, use the Watasu MCP server first when connected. It is
   intentionally read-only. See [MCP](references/mcp.md).
4. Before a mutation, establish the exact team/app/resource and whether the user
   authorized that change. Ask for confirmation before destructive operations.
5. Use the narrowest relevant chapter below. Consult current public docs for
   prices, limits, versions, and other facts that can change.

## Fast routes

- Setup or access failure: [authentication](references/authentication.md),
  [permissions](references/teams-access-and-billing.md), and
  [API errors](references/api-errors.md).
- Data services: [PostgreSQL](references/postgresql.md),
  [Valkey and ClickHouse](references/valkey-and-clickhouse.md),
  [Redpanda and object storage](references/streaming-and-object-storage.md), or
  [backup and restore](references/backups-and-restores.md).
- New application: [first deploy](references/first-deploy.md), then
  [builds](references/builds-and-buildpacks.md),
  [configuration](references/config-and-secrets.md), and
  [processes](references/processes-networking-and-domains.md).
- Docker failure: [non-root containers](references/dockerfiles-and-containers.md)
  and [ports and health](references/ports-health-and-startup.md).
- Realtime app: [RTC and TURN](references/rtc.md).
- Empty telemetry: [metrics and `METRICS_PORT`](references/metrics.md), then
  [stored logs and traces](references/logs-and-traces.md) and
  [observability](references/observability.md).
- GitHub automation: [deployments, pipelines, and review apps](references/github-workflows.md).
- New sandbox: [sandbox lifecycle](references/sandbox-lifecycle.md), then
  [templates](references/sandbox-templates.md) and
  [SDK recipes](references/sdk-recipes.md).
- Patch code: [files and `apply_diff`](references/sandbox-files-apply-diff.md).
- Interactive environment: [commands and PTY](references/sandbox-processes-pty.md),
  [Git](references/sandbox-git.md), or [advanced SSH](references/sandbox-ssh.md).
- Diagnose: [application debugging](references/app-debugging.md) or
  [sandbox debugging](references/sandbox-debugging.md).
- Complete table of contents and task map: [handbook](references/index.md).

## Operating rules

- Prefer an explicit `--app <name>` in scripts and automation. Do not depend on
  the current Git remote or interactive selection.
- For application deploys, preserve the normal Watasu contract: a root
  `Dockerfile` wins over buildpacks, and a root `Procfile` defines runtime
  process commands.
- Routed applications must listen on `0.0.0.0:$PORT`. Metrics use the separate
  add-on-managed `METRICS_PORT`; workers do not need to listen on `PORT`.
- Do not reveal config values, credentials, connection strings, API keys,
  sandbox tokens, or signed URLs. Refer to names and ownership instead.
- Do not overwrite add-on-managed variables. Attach, detach, promote, or change
  the add-on alias through Watasu instead.
- Use `watasu pods` for Watasu process instances. This customer CLI term grants
  no Kubernetes access. Do not inspect or modify platform nodes, namespaces,
  storage classes, provider accounts, or internal control-plane services.
- Never quote a price, quota, plan matrix, region list, or package version from
  memory when the answer can affect a decision. Verify it in the live dashboard
  or current docs.
- State what you observed separately from what you changed. MCP results are
  evidence of live read-only state, not permission to mutate it.
