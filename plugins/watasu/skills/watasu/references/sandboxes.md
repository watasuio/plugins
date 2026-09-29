# Sandboxes

Watasu sandboxes are isolated, programmable machines for agents, code execution,
and development workloads. Use the official SDK when possible; use the REST API
for integrations that need the raw contract.

For a guided route, continue through [lifecycle](sandbox-lifecycle.md),
[templates](sandbox-templates.md), [SDK recipes](sdk-recipes.md), and
[files with `apply_diff`](sandbox-files-apply-diff.md).

## Lifecycle

1. Select a team and template version (ID, tag, or latest).
2. Create with an idempotency key and bounded timeout/lifecycle.
3. Wait for create/connect to return a usable session or terminal failure.
4. Perform commands, file, Git, or network work through the data-plane session.
5. Pause when whole-machine state should be retained temporarily, or checkpoint
   disk state when a restorable artifact is required.
6. Destroy/release resources when explicitly requested and no longer needed.

REST mutations use a bearer API key and `Idempotency-Key`. Retain returned IDs.
Retry an ambiguous mutation with the same idempotency key, not a newly invented
one.

## Templates

Templates have immutable versions built from package specifications. Official
SDKs can turn a supported Dockerfile/package intent into a template build, but
do not assume the public REST API accepts arbitrary OCI images. Select versions
by immutable ID for reproducibility; tags/latest are convenient moving selectors.

Template inputs may include packages, setup commands, environment defaults, and
other documented build settings. Do not bake credentials into template layers.

## Create options

Create requests can set template version, timeout/lifecycle, metadata,
environment names/values, volume mounts, network policy, and exposed ports.
Classify environment values as sensitive and avoid logging the request body.
Use metadata for correlation, not secrets.

## Commands and PTY

The data plane supports command execution, streaming stdout/stderr, process
status, and PTY sessions. Bound commands with timeouts. An open WebSocket is not
proof that the process succeeded; retain exit status and final output.

Executing customer code can be destructive. Get approval for commands that
modify persistent data, install unknown software, publish artifacts, or make
external changes.

## Files and Git

Supported file operations include reading, writing, listing, watching, batches,
and patches; SDK coverage varies. Prefer structured file APIs over shell
redirection. Git helpers cover clone/auth/status/branches/add/commit/pull/push,
remotes, and config.

Treat repository credentials as secrets. Confirm remote and branch before push.
Signed upload/download URLs are credentials with expiry; do not print or retain
them unnecessarily.

## Volumes

Volumes persist independently and can be mounted into a sandbox. Detached file
operations are supported, while conflicting writes may be refused when a volume
is attached to a live sandbox. Resolve attachment state rather than bypassing
the safety check. Deleting a volume is destructive and may remove the only copy
of data.

## Networking and previews

Apply the narrowest egress/network policy required by the task and update it
through the supported API. Exposed ports can receive explicit HTTP preview URLs.
A preview URL is a capability; scope and share it carefully.

Separate sandbox reachability, process listening address, network policy, and
application authentication when diagnosing connectivity.

## Pause, resume, checkpoints, and restore

- **Pause** preserves whole-machine execution state when supported. A fallback
  resume may restart from retained disk instead.
- **Checkpoint** captures restorable disk state, not live CPU/memory state.
- **Restore** creates a new sandbox from a checkpoint rather than rewriting the
  existing sandbox in place.

Keep old resources until the restored sandbox is validated and the user
authorizes cleanup.

## SSH

CLI shortcut and direct SSH forms include:

```sh
watasu ssh <sandbox>
ssh <sandbox>@box.watasu.io
```

Use the exact username grammar and host-key instructions in the current SSH
docs. Authentication can use the supported token/key enrollment flow. Sandbox
SSH is interactive access; it does not imply `scp`, SFTP, port forwarding, or
other unsupported SSH subsystems. Use file APIs and explicit previews instead.

## Billing hygiene

Set timeouts, use idempotency keys, and enumerate retained sandboxes, volumes,
templates, and checkpoints when investigating usage. Consult current dashboard
pricing before estimating cost. Never destroy retained state solely because it
appears idle without confirmation.

[Handbook](index.md) · [Advanced SSH](sandbox-ssh.md) · [Sandbox debugging](sandbox-debugging.md)
