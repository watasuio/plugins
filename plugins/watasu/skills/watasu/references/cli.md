# CLI

## Install and authenticate

Follow the current [CLI installation guide](https://docs.watasu.io/cli/install/)
for the user's platform, then:

```sh
watasu --version
watasu login
watasu whoami
```

Interactive login opens the browser. Follow [authentication](authentication.md)
for CI login, credential storage, scope, and revocation. Setting an SDK API-key
environment variable alone is not a replacement for CLI login.

## Selection rules

- Examples use `<placeholders>` for customer-selected values. Replace them
  before running a command; angle brackets are not literal shell arguments.
- Human interactive commands may infer an app from a Watasu Git remote.
- Scripts and CI must pass `--app <name>` explicitly.
- Pass team/resource IDs where names can collide.
- Use `--json` for machine-readable output when the command offers it.
- Run `watasu <command> --help` before relying on a flag that can drift.

## Command map

Use the current CLI reference for the complete map. Common task families are:

| Task | Commands |
| --- | --- |
| Identity and teams | `login`, `logout`, `whoami`, `teams` |
| Apps | `create`, `apps`, `destroy`, `rename`, `git:remote` |
| Deploy and releases | Git push; use MCP/dashboard for build and release state |
| Processes | `pods`, `pods scale`, `pods type` (`ps` aliases `pods`) |
| Config | `config`, `config set`, `config unset` |
| Logs/telemetry | `logs`, `metrics`, `traces` |
| Domains | `domains`, `domains add`, `domains remove`, `domains info`, `domains wait` |
| Add-ons | `addons` create/attach/detach/destroy/info/wait/backup/restore/promote groups |
| PostgreSQL | `pg psql` with optional `-c/--command`, plus info/wait/follow/backup/promote |
| Database clients | `valkey:cli`, `clickhouse:cli` |
| Private TCP trust | `apps:trust` on the server app |
| Self-service app access | `apps:join`, `apps:leave`, `apps:lock`, `apps:unlock` |
| Access | `members`, `access` and their add/update/remove operations |
| Sandboxes | `ssh` for template/version or sandbox-ID targets |

Confirm the installed CLI's exact noun, flags, and argument order. Some colon
commands are supported but hidden from top-level help; use their own `--help`.
For dashboard-only operations, see [supported surfaces](capabilities.md).

## Current telemetry forms

```sh
watasu metrics --query '<promql>' --since <duration> --app <app>
watasu metrics --query '<promql>' --at <unix-seconds> --app <app>
watasu metrics --query '<promql>' --since <duration> --step <seconds> --app <app>
watasu traces --query '<traceql>' --since <duration> --limit <n> --app <app>
watasu traces --trace-id <hex-trace-id> --app <app>
watasu logs --query '<log-query>' --process-type <type> --app <app>
```

These reflect the current command family; still use `--help` for the installed
version.

## Remote commands and SQL

`watasu pg psql -c` and sandbox SSH commands can mutate customer data.
Inspection is not blanket authority to run arbitrary shell or SQL commands.
State the exact command, target app/add-on/sandbox, and expected side effect
before executing it.

## Automation failures

On an authentication failure, verify identity and scope without printing the
credential. On ambiguous app selection, add `--app`. On unsupported flags,
compare the installed `watasu --version` with current docs and installed help
instead of retrying variants blindly.
