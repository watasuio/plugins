# Valkey and ClickHouse

These services use ordinary application client libraries and Watasu-managed
connection variables. Their operational responsibilities stay with Watasu.

## Valkey

Use a Redis-protocol library and the managed `REDIS_URL` (or alias-prefixed
equivalent). Choose persistence, memory, and availability from the current
[Valkey plans](https://docs.watasu.io/addons/valkey/). A non-persistent cache has
no durable-data guarantee; select a persistent plan deliberately for queues or
sessions that must survive replacement.

```sh
watasu addons create valkey:<plan> --app <app>
watasu addons wait <cache-addon>
watasu valkey:cli <cache-addon> --app <app>
```

Check memory pressure, TTLs, eviction behavior, connection use, and client
timeouts. Avoid an unbounded key scan in production. Flush/delete commands are
destructive; opening the client does not authorize them.

## ClickHouse

Use a ClickHouse client for analytical/append-heavy workloads and the managed
`CLICKHOUSE_*` variables. Select the HTTP or native protocol supported by that
client, using Watasu's provided host/port/authentication values.

```sh
watasu addons create clickhouse:<plan> --app <app>
watasu addons wait <analytics-addon>
watasu clickhouse:cli <analytics-addon> --app <app>
```

Check the logical database/table, ingestion state, query scope, and protocol
before assuming a service failure. Bound exploratory queries by time and row
count. Schema/drop/truncate operations require explicit intent.

Both services use [replacement restores](backups-and-restores.md) on supported
plans. For exact variable names and aliases, consult the
[environment reference](https://docs.watasu.io/reference/addon-env-vars/).

[Handbook](index.md) · [Add-ons](addons-and-data.md) · [Backups](backups-and-restores.md)
