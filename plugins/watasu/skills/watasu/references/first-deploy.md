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
