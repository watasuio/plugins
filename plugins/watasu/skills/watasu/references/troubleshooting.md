# Troubleshooting

Diagnose by lifecycle layer and return evidence, not guesses.

Use the focused [application debugging](app-debugging.md) or
[sandbox debugging](sandbox-debugging.md) chapter for a concise decision tree.

## Evidence checklist

Collect the narrowest safe set:

- timestamp and time zone;
- team, app, process, add-on, or sandbox ID;
- source commit SHA;
- build and release IDs;
- exact command/request and sanitized error;
- process status and relevant bounded logs;
- domain/trust/preview state when networking is involved;
- client and CLI/SDK version.

Use MCP first for app identity and current read-only state when available.

## App decision tree

### No build was created

Check Git remote/repository connection, branch, commit SHA, auto-deploy setting,
and required checks for that exact SHA.

### Build failed

Inspect build output. Confirm root Dockerfile selection versus buildpacks,
dependency lockfiles, build context, architecture, and that no runtime-only
secret was incorrectly expected during build.

### Build succeeded, release failed

Inspect release output and `release`/group-release commands. Verify migrations
are repeatable and configuration/add-on variables exist by name without printing
values.

### Release succeeded, process is unhealthy

Inspect process formation and runtime logs. Confirm command, numeric user file
permissions, entrypoint/Procfile interaction, and `0.0.0.0:$PORT` for web.

### Process is healthy, request fails

For web, inspect managed/custom domain, DNS, TLS, host handling, and application
response. For TCP, inspect directional trust then protocol auth. For RTC, inspect
signaling, Watasu-provided TURN/ICE config, UDP, and replica-specific routing.

### Data service fails

Separate add-on health, attachment/alias, managed variable presence, network
reachability, credentials, database/topic/bucket existence, and application
client behavior. Do not expose connection values.

### Telemetry is empty

Separate “query returned no matches” from query/datasource failure. Verify time
window, labels, PromQL/TraceQL/log syntax, ingestion endpoint configuration, and
the release expected to emit the signal.

## Sandbox decision tree

### Create/connect failed

Retain request/sandbox/template IDs and terminal status. Retry an ambiguous
mutation with the same idempotency key. Do not add polling around a terminal
failure or create duplicate sandboxes with new keys.

### Command stream stalled

Check session expiry, WebSocket state, process status, and timeout separately.
Reconnect through the supported client; do not assume the command never ran.

### File or volume write failed

Check path, permissions, attachment state, and whether writes are refused while
the volume is live-attached. Do not bypass the guard with an unsafe shell write.

### Preview or outbound network fails

Check process listen address/port, exposed-port declaration, preview URL expiry,
network policy, DNS, and application auth independently.

### Resume differs from pre-pause state

Determine whether whole-machine resume succeeded or the documented disk-based
fallback restarted processes. Checkpoint restore creates a new sandbox and does
not preserve live memory state.

## Escalation packet

When the public contract cannot resolve the failure, prepare a support report
with sanitized identifiers, exact timestamps, the failed public operation, and
bounded output. Do not include tokens, config values, database URLs, signed
URLs, or internal-platform speculation.

[Handbook](index.md) · [Application debugging](app-debugging.md) · [Sandbox debugging](sandbox-debugging.md)
