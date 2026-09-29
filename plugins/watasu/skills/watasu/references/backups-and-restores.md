# Backups and restores

Use the Watasu CLI for managed PostgreSQL, persistent Valkey, and ClickHouse
backups. Availability and schedule/retention depend on the selected plan. Inspect
the actual backup status; an entry in a list is not proof capture finished.

## Capture and inspect

```sh
watasu addons backups <addon>
watasu addons backups capture <addon>
watasu pg backups DATABASE_URL --app <app>
watasu pg backups capture DATABASE_URL --app <app>
```

Capture is a write. Confirm the resource and the user's intent first. Use an
attachment variable name or add-on name, never a connection URL, as the database
selector.

## Restore and validate

```sh
watasu addons restore <source-addon> <backup-id-or-file> --name <replacement>
watasu addons wait <replacement>
```

Restore creates a replacement; it does not overwrite the source. Verify the
replacement's terminal ready state and data using its service client. If an app
attachment is needed for validation, explicitly select a validation app and
alias. Do not replace a production attachment merely to inspect restored data.

After the user authorizes switching the source's attachments:

```sh
watasu addons promote <replacement>
```

Inspect every affected app and its resulting release. An add-on can have more
than one attachment. Keep the original resource until removal is authorized.
Backup restore and PostgreSQL follower creation are different operations.

## Files and downloads

Use the current [backup format and upload limits](https://docs.watasu.io/workflows/backups-and-restores/)
before uploading a local file. Treat dumps as confidential customer data.

```sh
watasu pg backups download <backup-id> DATABASE_URL --app <app> --output <archive-path>
```

This downloads a physical PostgreSQL backup archive, not a SQL dump. Do not feed
it to `psql` or assume interchangeability with an application export. Confirm
format compatibility for the intended restore, protect the local archive, and
do not use `--force` to overwrite a file without authorization.

## Retention is not recovery

Redpanda, object storage, and observability services do not use this managed
backup/restore workflow. Replication is not protection against logical deletion.
Historical telemetry can be lost when its data add-on is removed. Preserve any
required exports before an authorized deletion.

[Handbook](index.md) · [Add-ons](addons-and-data.md) · [PostgreSQL](postgresql.md)
