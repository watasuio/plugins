# Sandbox Git automation

SDK Git helpers avoid fragile shell quoting and expose structured repository
state. They cover authentication, user configuration, initialization, clone,
status, branch create/delete, add, commit, reset, restore, pull, push, remotes,
config, and checkout.

## Safe sequence

1. Inspect the target directory and existing repository.
2. Authenticate with the narrowest credential using the SDK's explicitly
   dangerous authentication helper only when required.
3. Configure author identity deliberately.
4. Confirm remote URL and current branch.
5. Inspect status before changing files.
6. Apply structured writes or [`apply_diff`](sandbox-files-apply-diff.md).
7. Run checks, inspect diff, and commit only the intended files.
8. Push only with explicit user intent and a confirmed remote/branch.

Repository credentials, embedded remote credentials, and provider tokens are
secrets. Do not include them in logs, command output, commit messages, patches,
or sandbox metadata.

## REST payload conventions

Raw API payloads use documented snake_case fields. SDKs expose language-native
names. Do not guess a payload from a method name—consult the installed SDK types
or current API docs.

## Recovery

- Authentication failure: verify scope and identity without printing the token.
- Dirty worktree: preserve unrelated work and patch only intended paths.
- Push rejected: fetch/inspect divergence; do not force-push unless explicitly
  authorized.
- Interrupted clone/pull: inspect repository state before retrying.
- Ambiguous commit: compare HEAD, status, and diff; do not assume it landed.

[Handbook](index.md) · [Files](sandbox-files-apply-diff.md) · [Processes](sandbox-processes-pty.md)
