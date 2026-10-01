# Qdrant

Qdrant provides native vector and hybrid search. Check the live catalog before
proposing a billable resource. Consult the
[Qdrant documentation](https://docs.watasu.io/addons/qdrant/) for current availability.
Never assume an advertised tier or old example is available in the customer's team.

## Customer workflow

Use the generic `addons:create qdrant:PLAN`, `addons:info`, `addons:wait`, and
attachment commands. Establish the team and app first. Use native Qdrant clients;
there is no Watasu-specific database SDK or API proxy.

Attachment variables: `QDRANT_URL`, `QDRANT_GRPC_URL`, `QDRANT_API_KEY`,
`QDRANT_READ_ONLY_API_KEY`, `QDRANT_CA_CERT`. Aliases prefix them. Do not print values.
Private REST and gRPC connections require the supplied CA; never disable TLS
verification. Public access is optional and remains authenticated.

## Sizing and protection

- Plans specify peer count and per-peer CPU, RAM, and data disk. Replicas, payload
  indexes, WAL, and optimization consume capacity; physical disk is not unique data.
- Hobby is single-peer. Standard is three peers in one location. Premium spans
  three locations. Do not infer collection protection solely from the tier.
- Check fresh observed health, actual shard copies, replication factor, write
  consistency, and client ordering. Customers retain control of native settings.
- Qdrant OSS does not automatically reshard existing collections on peer growth.
  Reindex and switch a native alias when a different shard count is needed.
- Keep source documents/messages and an idempotent indexing pipeline. Qdrant
  search does not replace the application's authoritative database.

## Backups and restoration

Use generic capture/list/restore commands with a managed backup ID. Backups are
verified distributed shard snapshots with aliases and collection configuration;
they represent a capture interval, not database-wide point-in-time recovery.
Restore to a private replacement, wait for readiness, then validate counts,
payload filters, aliases, and search results with the native client.

Local-file restore and a single-file download are not supported. Never invent
these workflows. Promotion swaps attachments and retires the source; establish
explicit authorization before invoking it.

Use `watasu addons update ADDON --plan PLAN` for larger capacity. The destination
must retain at least the existing peer count, locations, CPU, memory, and disk per
peer. Billing changes after verification. Use the same command with
`--public-access true|false`, `--managed-placement true|false`,
`--backup-enabled true|false`, or `--backup-retention-days 1..35`.

Custom shard-key placement stays customer-managed; native backups and peer
replacement preserve its copy counts. API-key rotation can cause authentication
failures during the transition and invalidates JWTs signed with the old key.
Missing last copies or quorum cannot be repaired by inventing empty data.
