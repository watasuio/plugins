# Public API errors and retries

Prefer CLI/MCP for app operations and official SDKs for sandbox automation.
When using a documented sandbox REST operation, use `https://api.watasu.io/v1`,
a scoped bearer credential, and the documented request envelope. Session
responses contain credentials; consume them in code without printing them.

| Response or symptom | Customer action |
| --- | --- |
| 401 | Reauthenticate; verify credential expiry/revocation without displaying it |
| 403 | Verify team scope, app permissions, and any required billing state |
| 404 / missing resource | Check exact ID/name and visibility; do not infer global absence |
| 422 | Read structured validation details; correct shape or inspect returned quota |
| 429 | Honor `Retry-After`; use bounded backoff instead of rapid retries |
| Timeout / 5xx | Retain sanitized request ID and time; establish whether a mutation completed |
| Operation accepted but still pending | Inspect the resource's public status until a terminal outcome |

For sandbox mutations supporting `Idempotency-Key`, keep the same key and payload
for a retry of the same operation. A new logical operation gets a new key. Do
not assume every app endpoint or CLI write is idempotent; inspect state after an
ambiguous result before repeating it.

Sandbox create/connect/resume return a usable session or terminal failure. Do
not add readiness polling after success. Sandbox lifetime (`timeout`) is separate
from an HTTP request timeout; use the SDK's supported request settings. A
terminal error needs diagnosis, not another loop or new machine with a new key.

Preserve list filters and team scope when following `next_token`. Protect both
the account API key and the short-lived sandbox session token. Obtain a renewed
session through connect/resume; do not invent credentials or use direct host IPs.

When a public surface cannot resolve an error, report the affected resource,
timestamp, CLI/SDK version, request/build/release ID, and sanitized error to
Watasu support. Never attach credential files or raw environment dumps.

[Handbook](index.md) · [Authentication](authentication.md) · [Sandbox lifecycle](sandbox-lifecycle.md)
