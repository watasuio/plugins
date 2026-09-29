# Release commands and migrations

Release processes run once and gate rollout. They receive plain config, secret
runtime config, and attached add-on variables, but they are not routed services
and should not listen on `PORT`.

## Naming

```procfile
release: ./bin/migrate
web: ./bin/server
worker: ./bin/worker
jobs-release: ./bin/prepare-jobs
jobs-worker: ./bin/jobs
```

- `release` gates the entire release.
- `<group>-release` gates process types in that group.
- Processes outside a group are not implicitly gated by that group release.

Use a global release command for a schema change required by every process.
Use group-scoped gates only when the dependency is truly local to that process
family.

## Safe release work

- Make migrations idempotent or safely retryable.
- Bound lock acquisition and long-running data changes.
- Separate incompatible schema removal from code rollout.
- Avoid interactive prompts.
- Exit nonzero on failure and print a useful non-secret error.
- Keep the command compatible with the same non-root runtime as the app.

Do not run the migration from every web replica. Concurrency can corrupt data or
hold duplicate locks. Do not bypass a failed release by mutating the database
manually unless the user authorizes that exact recovery.

## Failure workflow

1. Identify the exact release and source image.
2. Read release output, not only runtime logs.
3. Verify required variable names and add-on attachment without printing values.
4. Determine whether the command is safe to retry.
5. Fix source or configuration and create a new release.

A failed release should leave the previous healthy release serving; verify that
state rather than assuming it.

[Handbook](index.md) · [Configuration](config-and-secrets.md) · [Application debugging](app-debugging.md)
