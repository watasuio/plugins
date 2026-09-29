# Sandbox debugging

Start with the object ID and the first failed contract: control plane, session,
process, file, network, or retained state.

## Create/connect/resume

- Record team, sandbox/request/template-version IDs and terminal status.
- Confirm the request fits live sandbox limits.
- Retry an ambiguous mutation with the same `Idempotency-Key`.
- Do not add polling after the SDK returns a usable session or terminal failure.
- A suspended billing account may block create/resume and data-plane mutations
  while still allowing pause/destroy; verify live account state.

## Command or stream

- Separate transport connection, process start, output events, and final exit.
- Reconnect with the last cursor to avoid gaps or duplicate replay.
- Inspect whether the process still runs before starting a copy.
- Check timeout and output truncation metadata.

## File, patch, or volume

- Confirm absolute working directory, path, encoding, permissions, and caps.
- Inspect the complete `apply_diff`/`applyDiff` report for partial failures.
- Check whether a volume is attached to a live sandbox before detached writes.
- Re-read changed content before claiming success.

## Network or preview

- Resolve DNS separately from egress policy and remote authentication.
- For preview, check public-traffic policy, port declaration, bind address, and
  current route token.
- Do not use unsupported SSH forwarding as a workaround.

## Resume or restore surprises

- A pause may resume whole-machine memory or use documented disk fallback.
- A checkpoint contains disk, not live memory.
- Restore creates a new sandbox ID.
- A volume has an independent lifecycle and may outlive both machines.

## Escalation packet

Provide sanitized IDs, timestamps, SDK/CLI version, exact public request, state,
and bounded output. Exclude API keys, data-plane tokens, signed URLs, Git
credentials, environment values, and untrusted file contents.

[Handbook](index.md) · [Lifecycle](sandbox-lifecycle.md) · [State and storage](sandbox-state-and-storage.md)
