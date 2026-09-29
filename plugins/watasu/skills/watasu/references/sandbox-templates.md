# Sandbox templates and Dockerfile conversion

A template is a reusable recipe. Each successful build creates an immutable
template version; tags and `latest` are moving selectors over those versions.

## Package specification

The reproducible template model can describe:

- APT, pip, and npm packages;
- setup commands;
- environment defaults;
- working directory and command/entrypoint intent;
- whether template construction may use internet or package registries.

Keep credentials out of template inputs and build output. Use runtime encrypted
environment values for sandbox-specific secrets.

## Version workflow

1. Create or select the team-owned template.
2. Submit a package specification.
3. Track build status and logs, using offsets for incremental retrieval.
4. Tag a successful immutable version when useful.
5. Pin the version ID in reproducible automation.

Provider-owned templates may be visible to customers but are not customer-owned
mutable recipes.

## Dockerfile import is translation

Official SDK helpers can parse supported Dockerfile instructions such as
`FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV`, `CMD`, and `ENTRYPOINT` into Watasu's
package-spec model. This is not an arbitrary OCI image import. Unsupported or
private-registry shapes fail closed rather than silently weakening provenance.

When conversion fails, reduce the Dockerfile to its durable package/setup
intent or write a package specification directly. Never pass registry passwords
through Dockerfile text.

## Template selection

- Version ID: deterministic and preferred for automation.
- Tag: readable but movable.
- `latest`: convenient for exploration, not reproducible.
- Snapshot: resumes from captured disk state and is a different artifact.

[Handbook](index.md) · [Lifecycle](sandbox-lifecycle.md) · [SDK recipes](sdk-recipes.md)
