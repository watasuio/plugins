# Redpanda and object storage

## Redpanda

Use Kafka-compatible clients with the broker list and authentication settings
in the attached add-on's managed variables. Select the current plan through
`watasu addons create redpanda:<plan> --app <app>` and wait for readiness.

Diagnose in order: broker connectivity, TLS/SASL configuration, topic existence,
producer acknowledgments, partition assignment, consumer group, and lag. Ordering
is per partition. Set topic retention and client retry/idempotence intentionally;
do not promise recovery of deleted topics or expired records. The managed add-on
does not provide the PostgreSQL/Valkey/ClickHouse backup API.

Customer Kafka clients operate on the service; no platform broker shell, operator,
or cloud account is required. See the [service contract](https://docs.watasu.io/addons/redpanda/).

## Object storage

Create `object-storage:<plan>` through `watasu addons create` and use an
S3-compatible SDK. Read the attached bucket, endpoint, region, and credentials
from managed environment variables. In particular, configure the provided
endpoint and honor `S3_FORCE_PATH_STYLE` when your SDK needs it. Do not assume
default AWS endpoints or that every SDK reads every exported variable.

Your application controls object access. Keep credentials server-side and use
short-lived signed URLs for private objects when appropriate. Verify bucket,
key, endpoint, region, addressing style, expiry, and browser CORS separately.
Use supported S3 operations for customer bucket settings; do not change platform
storage configuration to solve a browser upload failure.

Choose durability and egress allowances from the live catalog. Replication does
not undo deletion. Use application soft-deletes, distinct versioned object keys,
or deliberate exports where needed; do not assume an S3 feature is supported
without checking the current contract. Object storage is outside the managed
database backup workflow.

[Handbook](index.md) · [Add-ons](addons-and-data.md) · [Object storage docs](https://docs.watasu.io/addons/object-storage/)
