# Apps, deploys, and config

For an ordered path, start with [first deploy](first-deploy.md). The focused
chapters cover [build selection](builds-and-buildpacks.md),
[non-root images](dockerfiles-and-containers.md),
[configuration ownership](config-and-secrets.md), and
[`PORT` health](ports-health-and-startup.md).

## First deploy

```sh
watasu login
watasu create --team <team> <app>
git push watasu main
watasu logs --app <app>
```

If the Git remote already exists, inspect it before adding another. A deployment
can also come from a connected GitHub repository.

## Build selection

- Root `Dockerfile` present: Watasu builds it.
- No root `Dockerfile`: Watasu uses Cloud Native Buildpacks.
- Root `Procfile` present: its commands define process types for either build
  method.
- No `Procfile`: image/buildpack defaults determine the process, when available.

For a Dockerfile app:

- use a multi-stage build when it reduces the runtime image;
- run as a numeric non-root UID;
- keep runtime dependencies in the final stage;
- do not bake secrets into build arguments or layers;
- preserve image initialization with an entrypoint wrapper when Procfile commands
  need to run through the image's entrypoint;
- make the web server listen on `0.0.0.0:$PORT`.

Example Procfile:

```procfile
web: bin/start-web
worker: bin/start-worker
release: bin/migrate
```

## Deploy and inspect

Common commands:

```sh
watasu apps --all
watasu pods --app <app>
watasu logs --app <app>
```

Use MCP or the app dashboard for build and release state/output. Use build output
for compilation/image failures, release output for release-command failures, and
runtime logs for process failures.

## Configuration ownership

Classify every value before setting it:

- **plain config**: safe non-secret runtime setting;
- **secret config**: credential or sensitive value, available at runtime but not
  to the build by default;
- **add-on-managed config**: connection data created from an add-on attachment;
- **platform config**: values such as `PORT` or process/runtime metadata.

Plain values reach build, release, and runtime. Values marked secret are
deliberately excluded from build and become available to release/runtime. See
[configuration and secrets](config-and-secrets.md) before diagnosing a missing
build variable.

Typical operations:

```sh
watasu config --json --app <app> | jq -r '[(.config_vars // {} | keys[]), (.entries // [] | .[].key)] | unique[]'
watasu config set --plain KEY=value --app <app> --json | jq -r '[(.config_vars // {} | keys[]), (.entries // [] | .[].key)] | unique[]'
watasu config set --secret --file <private-env-file> --app <app> --json | jq -r '[(.config_vars // {} | keys[]), (.entries // [] | .[].key)] | unique[]'
watasu config unset KEY --app <app> --json | jq -r '[(.config_vars // {} | keys[]), (.entries // [] | .[].key)] | unique[]'
```

Check current `watasu help` for exact flags before scripting a secret change.
Never echo or log the value as part of diagnostics. Config changes create a new
release; treat them as deploy-affecting changes. Set/unset responses may also
print config values: filter or suppress successful output as described in
[configuration and secrets](config-and-secrets.md).

Do not use `config set` to replace an add-on-managed variable. Change the
attachment alias, promote the correct add-on, or detach/attach it through the
supported add-on operation.

## Formation and scaling

Formation sets replicas and pod size per process. Inspect current formation
before changing it and identify whether the process is routed, background, or a
release gate.

```sh
watasu pods scale web=2 worker=1 --app <app>
watasu pods type web=<current-pod-type> --app <app>
```

Watasu offers fixed-price and usage-billed Dynamic sizes. Dynamic bills measured
CPU and memory within the selected size's ceiling while keeping the process
running. It does not automatically change replica count or promise scale-to-zero.
Consult current docs/dashboard for sizes, ceilings, and prices. With two or more
replicas, Watasu spreads replicas across available failure zones when the
platform can do so.

## `app.json`

`app.json` is committed, non-secret app automation. It can describe config keys,
add-ons, formation, scripts, and review-app overrides. See
[GitHub workflows](github-workflows.md) for review apps and
[add-ons and data](addons-and-data.md) for service attachments.

Never put real secret values in `app.json`. Declare the variable and set its
value through Watasu or the CI secret store.

[Handbook](index.md) · [`app.json` reference](app-json.md) · [Application debugging](app-debugging.md)
