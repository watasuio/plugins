# Builds and buildpacks

A build converts a source revision into an immutable runnable image. It does not
apply runtime config or prove a process can become healthy.

## Build pricing and balance

App builds cost **€0.50/hour**, billed per actual running second, with limits of
**16 vCPU and 30 GiB memory**. Failed and canceled builds still charge for the time
the builder ran. Queueing, scheduling, and image pulling before the builder
starts are free. Promoting an existing image through a pipeline does not run or
charge for another build; deployed processes and other resources retain their
own charges.

Before a manual build, Git push, connected GitHub deploy, pipeline source build,
or review-app build, check the app's billing account in the dashboard. It needs
a positive available balance sufficient for at least one second. Zero or
insufficient balance blocks build work before source fetching; a successful
GitHub check alone does not guarantee a build starts. Personal teams use their
owner's billing account; shared teams use their team account. A saved payment
card is not required. Stripe top-ups have a **€5 minimum**.

Before starting a builder, Watasu reserves up to **€0.50** from available funds
for at most one hour. A smaller balance funds a shorter execution deadline.
Concurrent builds each reserve their own funds, so money held for one build is
not available to another build or resource. The dashboard distinguishes the
reserved amount from the final charge. When the builder stops, only its actual
running time is charged and the unused reservation is refunded. The hold is not
a one-hour minimum charge. Retries share the original one-hour execution limit.

Use the customer's dashboard top-up flow when needed; do not repeatedly retry
an unfunded build. See [billing](teams-access-and-billing.md) and the current
[public billing guide](https://docs.watasu.io/admin/billing-and-limits/).

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
