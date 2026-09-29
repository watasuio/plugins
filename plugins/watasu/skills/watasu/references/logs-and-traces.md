# Stored logs, live output, and traces

## Logs

Current CLI defaults query stored logs; `--tail` streams live process output.
These are distinct sources. Use the installed command's help if an older CLI
behaves differently.

```sh
watasu logs --app <app> --since 1h --num 100
watasu logs --app <app> --process-type worker --since 30m --query '|= "error"'
watasu logs --app <app> --start <unix-seconds> --end <unix-seconds> --forward --num 100
watasu logs --app <app> --tail --process-type web --num 20
```

Stored queries support LogQL and historical windows. Live tail supports line
filters, not arbitrary aggregation/parsing stages. `--dyno-name` targets an exact
instance returned by process inspection. Keep app/process filters and narrow
time windows; redact sensitive application output before sharing it.

Stored log availability and retention depend on the Logs add-on. If historical
queries fail or return no data, check the add-on, interval, filter, and ingestion.
Do not silently substitute a live tail and claim the historical incident is
clear. Build logs come from MCP/build output; they are separate from runtime logs.

## Traces

Attach Traces and instrument the application using OpenTelemetry. Use managed
`OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`, `OTEL_EXPORTER_OTLP_ENDPOINT`, and protocol
variables. Propagate trace context across requests and jobs, and include trace
IDs in structured logs without recording credentials or request bodies.

```sh
watasu traces --app <app> --query '{ duration > 1s }' --since 1h --limit 20
watasu traces --app <app> --trace-id <hex-trace-id>
```

Use either search or a trace ID. Historical searches also accept `--start` and
`--end`. A successful empty query does not prove no requests occurred: verify
sampling, exporter configuration, time range, and selected service.

## Grafana and retention

The first Logs/Metrics/Traces attachment provisions the app's Grafana workspace.
Use the returned customer URL. MCP can identify add-ons but does not query runtime
telemetry. In Grafana select Metrics for application metrics, Watasu Runtime for
process/managed-service metrics, and Watasu Object Storage for bucket metrics.

Grafana dashboards can outlive signal add-ons; removing a data add-on can delete
its historical data. Dashboard JSON alone does not provision Grafana. Removing
a repository dashboard file removes that managed dashboard on a successful
release; manually created dashboards with other UIDs remain separate.

[Handbook](index.md) · [Observability](observability.md) · [Metrics](metrics.md)
