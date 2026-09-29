# Sandbox lifecycle and API contract

Watasu sandboxes are isolated machines controlled through
`https://api.watasu.io/v1`, official SDKs, or SSH. Prefer an official SDK unless
an integration needs the raw HTTP/WebSocket contract.

## Before create

1. Resolve the team explicitly.
2. Read `sandbox_limits` for the current plan's allowed CPU, memory, disk,
   timeout, quotas, and current pricing.
3. Select an immutable template version for reproducible work.
4. Set a bounded timeout and `on_timeout` policy (`kill` or `pause`).
5. Choose network policy, mounts, exposed ports, and string metadata.
6. Store environment secrets securely; they are encrypted and not echoed back.

## Mutation discipline

REST uses a bearer `WATASU_API_KEY`. Mutating requests accept
`Idempotency-Key`. For an ambiguous timeout, retry with the same key so a client
does not create two machines. Keep sandbox, request, template-version, volume,
and checkpoint IDs.

Create, connect, and resume return only when a usable data-plane session exists
or the operation reaches a terminal failure. Do not add a polling loop or an
arbitrary client timeout around that contract.

## States and verbs

- `create`: make a new sandbox from a template/version or snapshot.
- `connect` / `resume`: obtain a usable session, resuming if necessary.
- `pause` / `stop`: retain the sandbox for later use.
- `destroy` / `kill`: permanently remove the sandbox.
- `list`: filter by metadata/state and follow `next_token` pagination.

Closing an SDK client or session is not the same as destroying the sandbox.
Make lifecycle cleanup an explicit policy.
Python's `with Sandbox.create(...)` and the async context manager are exceptions:
exiting the context kills the sandbox. Use a context manager only for an
explicitly disposable sandbox, not one that should be paused and reconnected.

The default timeout action is `kill`. Use `lifecycle.on_timeout: "pause"` for
retention and enable `auto_resume` only deliberately; a later request can resume
the machine and restart usage charges. Template `runtime_baseline` and live team
limits determine CPU/memory choices and plan-managed disk size. On
`sandbox_quota_exceeded`, inspect the returned quota snapshot before changing
shape or starting another sandbox.

## Failure-safe skeleton

```text
load API key from secret storage
read live sandbox limits
resolve team and immutable template version
create with one idempotency key and bounded lifecycle
receive usable session or terminal failure
perform bounded work and retain structured results
pause, checkpoint, or destroy only according to user intent
close transports in finally/defer/RAII
```

[Handbook](index.md) · [Sandbox overview](sandboxes.md) · [Templates](sandbox-templates.md)
