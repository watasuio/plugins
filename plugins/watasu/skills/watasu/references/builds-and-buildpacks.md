# Builds and buildpacks

A build converts a source revision into an immutable runnable image. It does not
apply runtime config or prove a process can become healthy.

## Builder selection

Watasu chooses from repository root:

1. A `Dockerfile` selects a Dockerfile build.
2. Without one, Cloud Native Buildpacks detect the project.
3. A root `Procfile` supplies process types for either path.
4. Without a Procfile, image or buildpack defaults may provide a process.

Keep build context small with `.dockerignore` or equivalent source hygiene. Do
not include release archives, local databases, editor state, credentials, or
dependency caches unless the builder explicitly needs them.

## What reaches the build

Plain app config variables are available to the build. Values explicitly marked
secret are excluded. Add-on-managed connection variables belong to runtime and
must not be treated as build inputs.

This commonly surprises frameworks that fetch private packages, precompile code
that reads runtime credentials, or generate static bundles from secret values.
The correct fix is to separate build-time public configuration from runtime
secrets. See [configuration and secrets](config-and-secrets.md).

## Reproducible builds

- Commit the language lockfile.
- Pin base images by a deliberate version or digest where appropriate.
- Keep network downloads deterministic and verify checksums for standalone
  artifacts.
- Put framework compilation in the build stage, not container startup.
- Do not rely on files outside the Git/build context.
- Emit useful errors without printing environment values.

## Diagnosing a failed build

1. Match the build to the exact commit SHA.
2. Confirm whether Dockerfile or buildpack selection occurred.
3. Find the first causal error, not the final wrapper error.
4. Check lockfiles, runtime/toolchain versions, architecture, and build context.
5. If a variable is missing, classify it as plain, secret, add-on-managed, or
   platform-managed before changing anything.
6. Reproduce the build with the same builder contract when practical.

Use build output for compiler/image failures. Runtime logs cannot explain a
container that was never built.

[Handbook](index.md) · [First deploy](first-deploy.md) · [Dockerfiles](dockerfiles-and-containers.md)
