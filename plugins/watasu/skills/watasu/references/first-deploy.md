# First deploy

This path takes a repository from source to a running Watasu app without
assuming a framework.

## 1. Make the application portable

- Commit dependency lockfiles.
- Choose either a root `Dockerfile` or buildpack detection.
- Add a root `Procfile` when the runtime command is not unambiguous.
- Make each routed process listen on `0.0.0.0:$PORT`.
- Keep credentials out of source, image layers, and build output.
- Ensure the runtime can start as a numeric non-root user.

Minimal Procfile:

```procfile
web: ./bin/server
worker: ./bin/worker
release: ./bin/migrate
```

Only declare process types the application actually needs.

## 2. Authenticate and create

```sh
watasu login
watasu whoami
watasu create --team <team> <app>
```

Creating resources and running formation can be billable. Confirm the team and
app name first. If the repository already has a `watasu` remote, inspect it
instead of silently replacing it.

## 3. Configure by ownership

Set non-secret values as plain config and credentials as secret config. Attach
managed services rather than copying their URLs by hand. Secret runtime config
does not enter the build phase; see [configuration and secrets](config-and-secrets.md).

## 4. Deploy

App builds are paid at €0.25/hour, billed per running second with 16 vCPU and
30 GiB limits. Check that the app's billing account has a positive available
balance sufficient for at least one second before pushing. Watasu reserves up
to €0.25, or less for a shorter funded deadline, and refunds unused funds after
the builder stops. A saved card is not required; Stripe top-ups start at €5.
See [build billing](builds-and-buildpacks.md#build-pricing-and-balance).

```sh
git push watasu main
```

The push starts a build and then a release. Those are distinct stages. A green
build does not prove release commands or runtime startup succeeded.

## 5. Validate

```sh
watasu pods --app <app>
watasu logs --app <app> --num 200
```

Validate the managed HTTPS hostname for a web process. Check the exact source
commit, build, release, process type, and response. For automation or a connected
repository, follow [GitHub workflows](github-workflows.md).

## Next

Read [builds and buildpacks](builds-and-buildpacks.md), then
[Dockerfiles and non-root containers](dockerfiles-and-containers.md).

[Handbook](index.md) · [Application track](index.md#application-track)
