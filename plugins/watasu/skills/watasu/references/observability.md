# Observability

## Start with the signal

- **Logs**: discrete application/runtime events and errors.
- **Metrics**: numerical time series queried with PromQL.
- **Traces**: request paths queried with TraceQL or by trace ID.

Use the signal matching the question, then correlate by app, process, release,
timestamp, and request/trace identifiers.

## CLI

```sh
watasu logs --app <app> --num 200
watasu logs --app <app> --process-type web --query '<log query>'
watasu metrics --app <app> --query '<promql>' --since 1h
watasu traces --app <app> --query '<traceql>' --since 1h --limit 20
watasu traces --app <app> --trace-id <hex-trace-id>
```

Use `--json` when available for automation. Verify exact flags with the current
CLI help. Bound time ranges and result counts so incident queries stay useful.
Current `watasu logs` queries stored history; `--tail` selects live output.
Read [logs and traces](logs-and-traces.md) for historical windows, filters,
instrumentation, and source-specific failure checks.

## Ingestion

- Applications write logs to their normal stdout/stderr path.
- A metrics add-on can receive Prometheus scraping on the platform-provided
  metrics port and supported remote-write/OpenTelemetry paths.
- A traces add-on can receive OpenTelemetry trace data.
- Grafana is the primary exploration surface for logs, metrics, and traces.

Use Watasu-provided endpoints and credentials. Never hardcode or publish them.
For exporter setup and empty-graph diagnosis, read
[metrics and `METRICS_PORT`](metrics.md).

## Repository dashboards

Commit Grafana dashboard JSON under `.watasu/dashboards/`. Directory structure
maps to folders. Each dashboard must have a title and a stable UID. Keep the
repository bundle within current documented file-count and size limits.

Use Watasu datasource placeholders instead of embedding datasource UIDs:

- `$watasu.metrics`
- `$watasu.runtime`
- `$watasu.object.storage`
- `$watasu.logs`
- `$watasu.traces`

Validate JSON and stable UIDs in CI. Do not commit datasource credentials. A
dashboard revision is deployed with the repository; correlate its commit/release
when diagnosing a stale dashboard.

## Evidence discipline

Report query, time window, app/process filters, and timestamp. Distinguish “no
matching data” from “datasource/query failed.” A healthy process list does not
prove telemetry ingestion, and a Grafana error does not prove an application
event occurred.

[Handbook](index.md) · [Metrics](metrics.md) · [Application debugging](app-debugging.md)
