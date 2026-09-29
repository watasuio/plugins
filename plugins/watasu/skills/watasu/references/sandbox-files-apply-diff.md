# Sandbox files and `apply_diff`

Use structured file methods instead of shell redirection. They preserve binary
data, structured errors, and safer path handling.

## Core file operations

Official SDKs cover reading, writing, listing, directory creation, stat, move,
delete, batched writes, watches, and signed uploads/downloads. Binary payloads
use bytes or explicit base64 according to the SDK/API. Signed URLs are temporary
credentials and must not be logged.

Rust also exposes native range reads, glob, grep, batched deletion, and explicit
byte/output caps. Check truncation metadata rather than treating a capped result
as the complete file.

## `apply_diff`

Use the SDK patch primitive for agent-authored source changes:

```python
report = sandbox.files.apply_diff(diff, cwd="/workspace/project")
```

```ts
const report = await sandbox.files.applyDiff(diff, {
  cwd: "/workspace/project",
});
```

```rust
let report = sandbox.files
    .apply_diff(diff, ApplyDiffOptions {
        cwd: Some("/workspace/project".into()),
        ..Default::default()
    })
    .await?;
```

The result is a structured patch report with status, per-file summaries, and
failures—not a boolean. Inspect every failed hunk/file before claiming success.
Use a stable absolute `cwd`, generate paths relative to it, and read the target
context before constructing the patch.

## Safe patch workflow

1. Read only the relevant ranges/files.
2. Generate a minimal patch in the format supported by the installed SDK.
3. Call `apply_diff` / `applyDiff` with the intended repository root.
4. Inspect the complete structured report.
5. Re-read changed ranges.
6. Run focused tests/formatters through the process API.
7. Inspect Git status/diff before any commit or push.

Do not silently fall back to a broad shell rewrite after a failed patch. Resolve
stale context, path, permissions, encoding, or partial-application state.

The SDK examples use this structured patch format; do not assume an ordinary
`git diff` is accepted without checking the installed implementation:

```text
*** Begin Patch
*** Update File: a.txt
@@
-alpha
+beta
*** End Patch
```

[Handbook](index.md) · [SDK recipes](sdk-recipes.md) · [Git automation](sandbox-git.md)
