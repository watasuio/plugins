# Metrics and `METRICS_PORT`

Watasu exposes platform metrics automatically and supports application metrics
through the Metrics add-on.

## Platform versus application metrics

Platform metrics—CPU, memory, restarts, OOM events, and managed-service signals—
do not require application instrumentation. Custom business/runtime metrics do.

When a Metrics add-on is attached, the runtime can inject:

```text
METRICS_PORT
OTEL_EXPORTER_OTLP_METRICS_ENDPOINT
OTEL_EXPORTER_OTLP_METRICS_PROTOCOL
PROMETHEUS_REMOTE_WRITE_URL
```

The default `METRICS_PORT` may currently be `9464`, but applications must read
the value instead of hardcoding it. It is add-on-managed and should not be
overridden with app config.

## Prometheus listener

Start a Prometheus-compatible endpoint, normally `/metrics`, on:

```text
0.0.0.0:$METRICS_PORT
```

Start it conditionally when `METRICS_PORT` exists so the image still runs
without the add-on. Each process type can expose its own metrics. Keep this
listener separate from customer traffic on `PORT` unless the application has a
deliberate combined-server design.

Metrics scraping is best-effort: failure to expose or scrape this endpoint does
not block application readiness or release. That is why an app can be healthy
while its custom graphs are empty.

## Other ingestion paths

Use the injected OTLP HTTP/protobuf endpoint or Prometheus remote-write URL when
the application's telemetry stack supports them better. Never print endpoint
credentials. Avoid enabling both paths accidentally and duplicating series.

## Empty graph checklist

1. Metrics add-on is attached and ready.
2. Expected variable names exist in the current release.
3. Process actually starts the metrics exporter.
4. Listener binds `0.0.0.0` on the injected `METRICS_PORT`.
5. Endpoint returns valid Prometheus exposition at the expected path.
6. Query time range and labels match the app/process/release.
7. Counter/rate query has enough samples.
8. Cardinality is bounded and label values are stable.
9. Grafana datasource/query succeeded rather than returning an ingestion error.

Use `watasu metrics --app <app> --query '<promql>' --since 1h` for a bounded
check. Distinguish no matching samples from datasource failure.

[Handbook](index.md) · [Observability](observability.md) · [Ports](ports-health-and-startup.md)
