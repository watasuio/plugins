# Add-ons and data

## Service catalog

Customer-facing stateful services include:

| Service | Typical use | Managed connection prefix |
| --- | --- | --- |
| PostgreSQL | Relational database | Alias-derived PostgreSQL variables |
| Valkey | Cache, queue, ephemeral data structures | Alias-derived Valkey variables |
| ClickHouse | Analytical database | Alias-derived ClickHouse variables |
| Redpanda | Kafka-compatible event streaming | Alias-derived Redpanda variables |
| Object Storage | S3-compatible objects | Alias-derived object-storage variables |
| Logs, Metrics, Traces | Observability ingestion and exploration | Service-specific variables |

Qdrant is an managed service; read [native search](qdrant.md) before proposing it.

Always inspect the current add-on catalog for available plans and regions.
Add-ons are team-owned resources with app attachments. Detaching or deleting an
ordinary app does not imply the add-on or its billing disappears. Inspect all
attachments before a destructive action. Review-app-managed resources have their
own lifecycle; do not generalize that automatic cleanup to shared add-ons.

For concrete workflows, read [PostgreSQL](postgresql.md),
[Valkey and ClickHouse](valkey-and-clickhouse.md),
[Redpanda and object storage](streaming-and-object-storage.md), and
[backups and restores](backups-and-restores.md).

## Aliases and environment variables

An attachment alias determines the environment-variable prefix. This supports
multiple resources of the same type. Treat those variables as add-on-owned:

- do not overwrite them with `config set`;
- do not copy connection strings between apps by hand;
- attach the add-on to the intended app under an intentional alias;
- promote/swap the supported resource when changing the primary service.

Use the current [add-on environment variable reference](https://docs.watasu.io/reference/addon-env-vars/)
for exact variable names. Do not print their values.

## Provision and attach

Before creating an add-on, establish team, app, service, region, plan, and alias.
Creation can incur charges. Use current `watasu addons --help` and service docs
for exact command forms. After attachment, deploy/release state may change as
managed variables become available.

## Backups and restores

The generic backup/restore workflow applies to PostgreSQL, Valkey, and
ClickHouse. Redpanda, Object Storage, and observability services do not inherit
that contract merely because they are add-ons.

Treat restore as replacement-oriented:

1. Identify source add-on and backup exactly.
2. Validate the backup format and current upload limit in the docs.
3. Restore into a replacement resource.
4. Validate the restored data through the service's client.
5. Promote/reattach only with explicit authorization.
6. Keep the old resource until the user authorizes its removal.

Uploaded backups currently have documented format and size constraints; verify
them live before transferring data. A completed upload is not proof that a
restore or promotion succeeded.

## Service-specific checks

- **PostgreSQL**: use `watasu pg psql` for an authorized database session or
  `-c/--command` for a bounded statement. Be careful with mutating SQL.
- **Valkey**: distinguish cache loss tolerance from durable workload
  requirements before restoring or replacing it.
- **ClickHouse**: validate database/table scope and analytical ingestion after
  restore.
- **Redpanda**: validate brokers, topics, consumer groups, and credentials using
  Kafka-compatible tooling without exposing secret config.
- **Object Storage**: validate endpoint, bucket, region, credentials, and signed
  URL expiry separately. Treat object deletion as destructive.

Provisioning success, attachment success, and application connectivity are
separate facts. Verify each layer.

## Outbound IP allowlists

If the customer needs stable outbound addresses, inspect whether the current
catalog offers `static-egress` for their app. This is app-scoped and cannot be
shared like a database attachment. Read the returned status and reserved address
set; `waiting_for_capacity` is not ready. The application can receive
`WATASU_STATIC_EGRESS_IP` and `WATASU_STATIC_EGRESS_IPS` once allocated. Allowlist
the full reserved set at the customer's destination, not an observed transient IP.
Build traffic is a separate lifecycle and must not be assumed to use those IPs.
For unavailable capacity or provisioning failure, contact support with the add-on
ID and public error. Availability must be verified before promising this feature.
