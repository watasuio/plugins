# Sandbox SDKs

Official SDKs expose the sandbox control plane and data plane with language-native
types. Prefer them over handwritten HTTP/WebSocket clients.

## Packages

Use current package documentation for versions:

```sh
pip install watasu
pip install watasu-code-interpreter
npm install @watasu/sdk
npm install @watasu/code-interpreter
cargo add watasu
```

The exact sync/async and feature coverage differs by language. Do not translate
an example mechanically without checking that SDK's current API.

## Shared contract

Across the official SDKs, the durable model is:

- authenticate with a Watasu API key without logging it;
- select a team explicitly;
- create/connect returns a usable session or terminal failure;
- list calls can be paginated and filtered;
- retain sandbox/template/version/checkpoint/volume IDs;
- stream command events until final exit status;
- close clients/sessions and release resources deliberately.

Do not add readiness polling after a successful create/connect result. Do not
hide terminal failures behind an arbitrary client timeout.

## Capability map

Depending on language and version, SDKs support:

- sandbox create, connect, inspect, list, pause, resume, kill, and destroy;
- streaming commands, process output, stdin, signals, and PTY;
- file read/write/list/watch, batches, patches, glob/grep/range operations;
- Git clone/auth/status/branches/add/commit/pull/push/remotes/config;
- signed upload/download URLs;
- persistent volume lifecycle and mounts;
- metrics, snapshots/checkpoints, restore, and cleanup;
- live network-policy updates and exposed-port previews;
- template builds from package specifications and supported Dockerfile parsing;
- tags, version selection, and build status;
- an MCP gateway running inside a sandbox;
- persistent Code Interpreter contexts with structured results, logs, and
  language errors.

Check the chosen package before promising one of these methods.

All three full SDKs expose the structured patch primitive:
Python `files.apply_diff`, TypeScript `files.applyDiff`, and Rust
`files.apply_diff`. See the complete [`apply_diff` guide](sandbox-files-apply-diff.md).

## Minimal implementation pattern

Language syntax varies, but preserve this structure:

```text
load API key from secret storage
construct client
resolve team and immutable template version
create sandbox with idempotency key and timeout
receive usable session
perform bounded work and capture exit/result
checkpoint or persist only if requested
close session/client
destroy sandbox only when lifecycle policy or user intent says to
```

Use `try/finally`, `defer`, or RAII for connection cleanup. Distinguish closing a
client from destroying a sandbox.
Python sync/async sandbox context managers kill the sandbox on exit. Choose them
only when deletion is the intended cleanup; see [SDK recipes](sdk-recipes.md).

## Code Interpreter

Code Interpreter contexts keep language state across executions. Capture the
structured result, logs, and error independently. A transport-successful call
can contain a language/runtime error. Do not concatenate untrusted values into
code; pass data through supported bindings/files where possible.

## Template and Dockerfile handling

Package-spec template builds are the canonical reproducible path. Where an SDK
offers Dockerfile parsing, it translates supported intent into the template
model; it is not evidence that arbitrary images can be imported through every
API. Keep template build inputs non-secret and pin immutable versions in
reproducible automation.

## Network and credential safety

- begin with the narrowest network policy;
- treat preview URLs, session tokens, Git credentials, and signed URLs as
  secrets;
- keep API keys in environment/secret stores, never examples or source;
- make external side effects explicit in agent tools;
- require confirmation before push, publish, deletion, or persistent-data
  mutation.

[Handbook](index.md) · [SDK recipes](sdk-recipes.md) · [Sandbox MCP and Code Interpreter](sandbox-mcp-code-interpreter.md)
