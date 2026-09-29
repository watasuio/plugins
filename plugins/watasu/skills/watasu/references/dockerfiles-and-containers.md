# Dockerfiles and non-root containers

Watasu runs application containers as a non-root user without privileged
capabilities. Buildpacks account for this automatically; custom images must
also work as a numeric non-root UID.

## Reliable Dockerfile pattern

```dockerfile
FROM <builder-image> AS build
WORKDIR /src
COPY . .
RUN <deterministic-build-command>

FROM <alpine-based-runtime-image>
RUN addgroup -S -g 10001 app \
 && adduser -S -D -H -u 10001 -G app app
WORKDIR /app
COPY --from=build --chown=10001:10001 /src/<artifact> /app/
USER 10001:10001
CMD ["/app/bin/server"]
```

The shown user-creation syntax is for Alpine-based images; use the equivalent
`groupadd`/`useradd` form on Debian-family images. A numeric `USER` is safest
because the runtime can verify it is non-root. Ensure every file the process must read is
readable and every directory it must write is owned by that UID/GID.

## Filesystem and port rules

- Write temporary data only to writable application or temporary directories.
- Do not expect write access to image-owned root directories.
- Do not bind privileged ports; use the injected `PORT`.
- Bind routed listeners to `0.0.0.0`, not `127.0.0.1`.
- Persist durable data in a managed service, not the container filesystem.

## Procfile and entrypoint interaction

When a Procfile supplies a command, Watasu runs it through:

```text
/bin/sh -lc '<procfile command>'
```

That means the final image must contain `/bin/sh`, environment expansion occurs,
and the Procfile command replaces the image's normal entrypoint/CMD behavior.
If the image depends on an entrypoint wrapper, call it explicitly:

```procfile
web: /docker-entrypoint.sh nginx -g 'daemon off;'
```

A distroless image can work when its image defaults define the process and no
shell-backed Procfile command is required. It will fail when a Procfile command
expects `/bin/sh`.

## Boot-failure checklist

- numeric non-root user exists;
- executable bit and ownership survived `COPY`;
- runtime libraries are in the final stage;
- working directory and relative paths match;
- `/bin/sh` exists when a Procfile is used;
- entrypoint initialization is not skipped;
- routed service binds `0.0.0.0:$PORT`;
- metrics listener, if enabled, uses `METRICS_PORT`.

[Handbook](index.md) · [Builds](builds-and-buildpacks.md) · [Ports and health](ports-health-and-startup.md)
