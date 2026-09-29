# `app.json`

Root `app.json` is committed, non-secret provisioning intent. It is the source
of truth for review-app bootstrap and can describe ordinary app defaults.

## Top-level model

```text
name, description, logo, website, repository, keywords, success_url
env, addons, formation, scripts, environments
```

## Environment declarations

```json
{
  "env": {
    "APP_MODE": { "value": "production" },
    "SECRET_KEY": { "generator": "secret" },
    "API_TOKEN": {
      "required": true,
      "description": "Token supplied during bootstrap"
    }
  }
}
```

Do not put a real secret in `value`. Use a generator or a required prompt, then
manage the actual runtime value through the supported secret surface.

## Add-ons and formation

Add-ons accept the documented service or `service:plan` identifier. Formation
maps Procfile process types to quantity and pod size. Plan and size identifiers
change; select them from current docs/dashboard rather than copying a dated
example.

## Lifecycle scripts

- `postdeploy`: once after the first successful deploy; keep it idempotent.
- `pr-predestroy`: cleanup before a review app is removed; scope it to the
  review environment and tolerate retry.

Long-lived release migrations still belong in a Procfile release command. Do
not overload first-deploy bootstrap with work required on every release.

## Review overrides

`environments.review` merges over top-level `env`, `addons`, `formation`, and
`scripts`. Use it for isolated review configuration and intentionally smaller
resources. Never point a review app at production data merely because a variable
is easier to reuse.

Validate JSON in CI and test the manifest through a real non-production review
app before depending on teardown hooks.

[Handbook](index.md) · [GitHub workflows](github-workflows.md) · [Configuration](config-and-secrets.md)
