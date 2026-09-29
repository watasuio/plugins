# PostgreSQL

Pick a current plan for connection count, capacity, backup retention, and
availability requirements. Use the [public catalog](https://docs.watasu.io/addons/postgresql/)
instead of prescribing a deployment topology.

## Provision and connect

```sh
watasu addons create postgresql:<plan> --app <app>
watasu addons wait <returned-addon-name>
watasu pg info DATABASE_URL --app <app>
watasu pg psql DATABASE_URL --app <app>
```

The create operation attaches the new add-on. Runtime variables include
`DATABASE_URL` and PostgreSQL client variables such as `PGHOST` and `PGPASSWORD`.
Read these from the app environment. Do not print their values or copy them into
source. The CLI opens a supported customer database session without platform
host access. Use `-c/--command` for bounded authorized SQL; never dump tables or
query secrets just to prove connectivity.

For a second database, attach it under an alias:

```sh
watasu addons attach <reporting-addon> --as REPORTING --app <app>
watasu pg psql REPORTING_DATABASE_URL --app <app>
```

Selectors are environment-variable names or add-on names, not URL values.

## Read followers

```sh
watasu pg follow DATABASE_URL --app <app> --name <follower> --plan <supported-plan>
watasu addons wait <follower>
```

Verify the plan supports followers and inspect readiness/replication lag before
using one for read-heavy work. Attach it under a distinct alias. A follower is
not an independent backup, and an asynchronous read can lag the primary.

## Diagnose application errors

Separate attachment/alias selection, variable presence, network connectivity,
authentication, connection exhaustion, and SQL/schema errors. Budget connection
pools across all replicas and workers. Migrations run through the application's
release command with runtime credentials. Use the supported backup workflow for
capture, restore, and promotion.

[Handbook](index.md) · [Backups](backups-and-restores.md) · [Configuration](config-and-secrets.md)
