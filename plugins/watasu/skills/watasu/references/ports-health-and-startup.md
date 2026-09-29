# `PORT`, health, and startup

`PORT` is the application traffic contract for service-exposed process types:
`web`, `*-web`, `*-tcp`, and `*-rtc`. Background workers and release commands do
not need an application listener and should not assume `PORT` exists.

## Listener contract

```text
host: 0.0.0.0
port: integer from the PORT environment variable
```

Do not hardcode a port, bind only to localhost, or select a random port. The
platform routes traffic and performs startup/readiness/liveness checks against
the injected port.

Watasu's application health contract checks TCP acceptance, not a framework's
`/health` response. Open the socket only after the process is ready to serve.
A process that accepts TCP but is internally wedged can still look healthy, so
application metrics and request probes remain useful.

## `PORT` is not `METRICS_PORT`

`PORT` carries customer/application traffic. A metrics add-on injects
`METRICS_PORT` for a Prometheus-compatible listener, normally exposing
`/metrics`. The listeners are normally separate and the application should read
both values from the environment. See [metrics](metrics.md).

## Startup design

- Run compilation and asset generation in the build, not on every boot.
- Run schema migration in a release command, not in every replica.
- Keep boot deterministic and bounded.
- Handle termination signals and stop accepting work before exit.
- Use stdout/stderr for logs.
- Avoid a supervisor that daemonizes the real process and hides its exit code.

## Diagnosis

If a process never becomes ready, check in order:

1. final command and working directory;
2. non-root permissions and executable bit;
3. listener uses the actual `PORT` value;
4. listener binds `0.0.0.0`, not localhost;
5. process opens the socket before health deadlines;
6. initialization is not waiting for a missing runtime dependency;
7. crash/restart reason in bounded logs.

Do not add a fake listener to a worker merely to satisfy a health model that
does not apply to it.

[Handbook](index.md) · [Dockerfiles](dockerfiles-and-containers.md) · [Metrics](metrics.md)
