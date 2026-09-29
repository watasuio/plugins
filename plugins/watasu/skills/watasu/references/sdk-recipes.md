# Sandbox SDK selection and recipes

Use the current package version rather than freezing a version in generated
instructions:

```sh
pip install watasu
pip install watasu-code-interpreter
npm install @watasu/sdk
npm install @watasu/code-interpreter
cargo add watasu
```

Python offers synchronous and asynchronous clients, TypeScript is ESM-oriented,
and Rust is asynchronous with Tokio. All preserve the same usable-session-or-
terminal-failure lifecycle contract.

## Choose the surface

- Full SDK: lifecycle, files, processes, Git, network, templates, storage.
- Code Interpreter package: persistent language contexts and structured results.
- SSH: human or shell-native interactive development.
- REST/WebSocket: custom integration where the SDK cannot be used.

## Standard automation recipe

```text
client = construct from WATASU_API_KEY
limits = read live sandbox limits
version = resolve immutable template version
sandbox = create(team, version, idempotency key, timeout, lifecycle)
session = sandbox's already-usable session
result = run bounded operation
check transport status, structured result, logs, and exit/error separately
close session/client
apply explicit pause/checkpoint/destroy policy
```

## Language mapping

Method naming follows language conventions. For example:

| Operation | Python | TypeScript | Rust |
| --- | --- | --- | --- |
| Apply patch | `files.apply_diff(diff, cwd=...)` | `files.applyDiff(diff, {cwd})` | `files.apply_diff(diff, ApplyDiffOptions { cwd, ... })` |
| Write files | `files.write_files(...)` | `files.writeFiles(...)` | `files.write_files(...)` |
| Signed upload | SDK signed-URL helper | SDK signed-URL helper | SDK signed-URL helper |

Check the installed SDK's generated docs/types for request shapes. Do not
translate snake_case payload fields to guessed camelCase when using REST.

## Disposable Python task

This example creates a billable sandbox and destroys it on context exit. Use it
only when the user requested disposable execution. Supply `WATASU_API_KEY` and
`WATASU_TEAM` through the user's environment, not literal code values.

```python
import os
from watasu import Sandbox

with Sandbox.create(team=os.environ["WATASU_TEAM"], timeout=300) as sandbox:
    sandbox.files.write("/tmp/hello.py", "print(2 + 2)\n")
    result = sandbox.commands.run("python /tmp/hello.py")
    print(result.stdout)  # Safe here: this example only prints a calculation.
```

For a retained workspace, create/connect without `with` and call `beta_pause()`
when retention is intended. Do not enter a context manager on an existing
sandbox that the user expects to keep.

## Disposable TypeScript task

Python lifetime is in seconds; TypeScript `timeoutMs` is in milliseconds.

```ts
import { Sandbox } from "@watasu/sdk";

const team = process.env.WATASU_TEAM;
if (!team) throw new Error("Set WATASU_TEAM before creating a sandbox");
const sandbox = await Sandbox.create({ team, timeoutMs: 300_000 });
try {
  await sandbox.files.write("/tmp/hello.js", "console.log(2 + 2)\n");
  const result = await sandbox.process.startAndWait("node /tmp/hello.js");
  console.log(result.stdout);
} finally {
  await sandbox.kill();
}
```

The selected template must contain the command's language runtime. For Rust,
async Python, template builds, and richer process options, use the public
[Python](https://github.com/watasuio/sdk/tree/main/python),
[TypeScript](https://github.com/watasuio/sdk/tree/main/ts), and
[Rust](https://github.com/watasuio/sdk/tree/main/rust) SDK examples together with
the installed package types. No Watasu platform checkout is needed.

## Error handling

- An HTTP/WebSocket failure is a transport/control-plane error.
- A command can start successfully and exit nonzero later.
- A Code Interpreter call can succeed while its language result contains an
  exception.
- Stream reconnect can replay output; use cursors and avoid duplicate handling.
- Output may be capped/truncated; inspect SDK metadata, especially in Rust.

[Handbook](index.md) · [SDK capability map](sandbox-sdks.md) · [`apply_diff`](sandbox-files-apply-diff.md)
