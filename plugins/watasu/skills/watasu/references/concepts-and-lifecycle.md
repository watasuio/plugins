# Concepts and lifecycle

Use the right object before choosing a command.

## Core app objects

- **Team**: billing and access boundary that owns apps and sandboxes.
- **App**: stable application identity, configuration, domains, collaborators,
  and deployment history.
- **Build**: source converted into an immutable runnable image. A root
  `Dockerfile` selects Dockerfile builds; otherwise Watasu uses buildpacks.
- **Release**: the image plus config, process formation, and add-on attachments
  that should run. Deploys and config changes create releases.
- **Process type**: a named command such as `web`, `worker`, `release`, or
  `api-rtc`, normally declared in `Procfile`.
- **Formation**: replica count and pod size for each process type.
- **Add-on**: a managed service attached to an app under an alias that determines
  its environment-variable prefix.
- **Pipeline**: ordered app stages that promote the same built artifact.
- **Review app**: temporary app created for a pull request from `app.json`.

The normal application path is:

```text
source -> build -> release -> process formation -> routed service
```

Do not confuse a successful build with a successful release. A release command
can gate rollout, and a running process can still fail readiness or routing.

## Sandbox objects

- **Template**: reusable build recipe and defaults.
- **Template version**: immutable built version selected by ID, tag, or latest.
- **Sandbox**: isolated machine created from a template version.
- **Session**: short-lived data-plane URL/token used for commands and files.
- **Volume**: persistent filesystem that can outlive a sandbox.
- **Checkpoint**: restorable disk state. It is not the same as pausing a whole
  machine.
- **Code Interpreter context**: persistent language execution context within a
  sandbox.

The normal sandbox path is:

```text
package spec or Dockerfile -> template version -> sandbox -> session -> work
```

Official SDK create/connect calls complete only when the session is usable or a
terminal failure is returned. Do not add client-side readiness polling unless a
specific API contract requires it.

## Identity rules

Names help humans; IDs disambiguate operations. Retain IDs returned by APIs and
use them for destructive or asynchronous actions. A Git remote can imply an app
interactively, but automation should name the app explicitly.
