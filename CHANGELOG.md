# Changelog

## 1.2.6

- Align the billing reference with the 16 vCPU and 30 GiB app-build limits.

## 1.2.5

- Increase app-build limits to 16 vCPU and 30 GiB, keeping the 60-minute cap
  and €0.50/hour rate billed by actual running seconds.

## 1.2.4

- Document positive balance admission for all add-ons, including free plans,
  implicit Grafana, app-create and app.json provisioning, restores, and followers.
- Clarify that an unsuspended zero balance still permits empty app creation.

## 1.2.3

- Document the positive wallet balance required before sandbox creation,
  checkpoint restore, and restarting stopped runtime, without a saved-card gate.
- Explain `sandbox_balance_required` and preserve existing sandbox runtime and
  storage pricing, metering, and cleanup behavior.

## 1.2.2

- Document paid app builds at €0.50/hour with 8 vCPU and 15 GiB limits, charged
  per running second, including failed and canceled builds.
- Explain prepaid reservations, unused-fund refunds, balance checks across
  manual and automatic build triggers, and free image-only promotions.
- Add build-funding prerequisites to agent setup and first-deploy guidance.

## 1.2.0

- Add hosted MCP write-tool workflows using the existing `read` and `write` scopes.
- Cover app, configuration, access, domain, add-on, backup, observability, terminal, and sandbox command tools.
- Document stream ownership and expiry, sensitive results, OAuth consent, and current protocol compatibility.
- Keep client-local credentials, Git operations, and interactive SSH on their supported surfaces.

## 1.1.0

- Add managed Qdrant plans, native REST/gRPC connections, observed replication,
  capacity changes, backups and replacement restores to the customer handbook.
- Document the add-on settings update command and Qdrant attachment variables.

## 1.0.0

- Publish the customer handbook and read-only MCP connection for Claude Code
  and Codex through the public Watasu marketplace.
- Map all 45 public documentation pages to focused handbook chapters.
- Correct MCP resource paths, CLI version syntax, Dynamic billing terminology,
  sandbox patch format, and Python context-manager cleanup guidance.
- Add authentication, supported-surface routing, database clients, backup
  downloads/restores, stored logs, traces, API error handling, and SDK recipes.
- Keep configuration values out of diagnostic output and explain customer
  dashboard handoffs where CLI/MCP do not provide an operation.

The plugin operates through customer interfaces and does not require Watasu
infrastructure access or private platform source code.
