# Supported customer surfaces

Start with the connected CLI and MCP. An installed plugin does not imply access
to platform internals or authorize writes. A Watasu account and the appropriate
team/app permissions are required.

| Task | Supported path |
| --- | --- |
| Identity, teams, apps, health, builds, current release, add-on state | Read-only MCP; CLI where available |
| Create/rename/delete apps, config, process sizes/counts, domains, trust | Watasu CLI |
| Deploy the user's source | Git remote created by the CLI; connected GitHub repository |
| Runtime logs, PromQL, TraceQL | Watasu CLI; customer Grafana for interactive exploration |
| Add-on create/attach/detach, backups, restores, followers, database sessions | Watasu CLI |
| Team members and app access | Watasu CLI; dashboard for invitations and pipeline roles |
| GitHub connection, auto-deploy settings, pipelines, promotions, review-app settings | Customer dashboard; repository `app.json` for review provisioning |
| Billing, payment methods, team creation, API keys, account security, notification preferences, integrations/webhooks | Customer dashboard |
| Sandbox interactive development | `watasu ssh` or customer sandbox SSH |
| Sandbox lifecycle, templates, files, processes, volumes, checkpoints, previews | Public sandbox SDK/API |
| Platform failure beyond customer diagnostics | Sanitized support report |

If the user has only CLI/MCP, finish the supported inspection and prepare any
repository changes. Explain the exact customer dashboard step the user needs to
perform. Do not guess an undocumented API, a new CLI verb, or a write-capable MCP
tool to fill a gap.

## Choosing apps or sandboxes

Apps fit long-running web services, workers, private TCP, and realtime services
deployed from a repository. Sandboxes fit temporary development, agents, code
execution, and isolated automation. Sandbox root access applies only to that
user-owned machine, not to Watasu infrastructure.

## Placement and plans

Read the current [regions](https://docs.watasu.io/reference/regions/),
[process sizes](https://docs.watasu.io/reference/pod-sizes/), and
[add-on catalog](https://docs.watasu.io/reference/addon-plans/) before selecting
resources. A CLI flag or code path does not prove a region/plan is offered to the
user. For data-residency requirements, verify the public contract with support.

[Handbook](index.md) · [Authentication](authentication.md) · [Customer boundaries](customer-boundaries.md)
