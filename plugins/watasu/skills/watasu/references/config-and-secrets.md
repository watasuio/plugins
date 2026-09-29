# Configuration and secrets

Configuration behavior depends on who owns a variable and in which lifecycle
phase it is needed.

| Kind | Build | Release command | Runtime | Owner |
| --- | --- | --- | --- | --- |
| Plain app config | Yes | Yes | Yes | Customer |
| Secret app config | No | Yes | Yes | Customer |
| Add-on-managed config | No | Yes | Yes | Watasu add-on attachment |
| Platform config such as `PORT` | No | As applicable | Selected process | Watasu |

## The build-secret boundary

`watasu config set --secret` deliberately excludes a value from Dockerfile and
buildpack execution. It becomes available to release commands and runtime
processes. This prevents a secret from casually entering image layers, build
caches, compiler output, or static assets.

Do not work around this by committing the value, turning it into a Docker
`ARG`/`ENV`, embedding it in `app.json`, or printing it from a build script. If a
build truly needs a private credential, use a secure external build/vendor step
or ask support for a documented supported path. Keep credentials classified as
secrets. Plain variables are exposed to the build and its artifacts.

## Runtime configuration

```sh
watasu config --json --app <app> | jq -r '[(.config_vars // {} | keys[]), (.entries // [] | .[].key)] | unique[]'
watasu config set --plain LOG_LEVEL=info --app <app> --json | jq -r '[(.config_vars // {} | keys[]), (.entries // [] | .[].key)] | unique[]'
watasu config set --secret --file <private-env-file> --app <app> --json | jq -r '[(.config_vars // {} | keys[]), (.entries // [] | .[].key)] | unique[]'
watasu config unset OLD_KEY --app <app> --json | jq -r '[(.config_vars // {} | keys[]), (.entries // [] | .[].key)] | unique[]'
```

Use current CLI help for exact installed syntax. Never paste a real value into
chat, issue text, logs, or shell transcripts. Validate presence by variable
name and application behavior, not by echoing it. The names-only command needs
`jq`; its filtering must happen in the same local invocation, before output is
returned to an agent. Config list, set, and unset can all print effective values;
filter their JSON output locally or suppress successful output during mutations.
Never return an unfiltered config response to chat.
In automation, enable the shell's `pipefail` option so a failed CLI operation
cannot be hidden by a successful output filter.

The private dotenv file must already be securely supplied by the user or secret
store, outside source control, with user-only permissions. Do not create it by
asking for secrets in chat. `--secret` and `--plain` are mutually exclusive;
omitting both preserves an existing key's classification and defaults a new key
to plain. Only the app owner can read/change app-owned secret values; a maintainer
can manage plain config but sees another owner's secret as a redacted key.

## Managed variables

Do not set or override `PORT`, TURN variables, or add-on connection variables.
Do not override `METRICS_PORT` when the metrics add-on manages it. Attach,
detach, promote, or rename the owning resource through Watasu so the complete
variable set stays consistent.

## Framework traps

- Static frontend builds expose build-time values to every browser; never put a
  secret there.
- Rails, Phoenix, Node, and similar compile steps should not require database or
  API credentials merely to produce an artifact.
- Generate runtime configuration on process boot when it genuinely depends on a
  secret.
- Keep release migrations in a release process, where runtime secrets and
  add-on variables are available.

Config changes create a new release. Correlate the resulting release before
declaring the change active.

[Handbook](index.md) · [Builds](builds-and-buildpacks.md) · [Release commands](release-commands-and-migrations.md)
