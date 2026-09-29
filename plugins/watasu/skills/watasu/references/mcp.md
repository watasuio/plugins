# MCP

The plugin connects to:

```text
https://mcp.watasu.io/mcp
```

It is a remote HTTP MCP server. OAuth is the preferred interactive
authentication method. The user consents to all or selected teams, and the
client manages short-lived access plus refresh. Headless clients can use a
Watasu API key as a bearer token when supported.

## Security model

The MCP server is intentionally read-only. It does not expose config values,
database credentials, billing details, runtime log bodies, or write tools. Never
attempt to turn an MCP resource into an undocumented mutation.

MCP visibility proves the authenticated principal can read the selected team;
it does not authorize a CLI/API write. Obtain mutation intent separately.

## Resource map

Available resources include these stable families:

```text
watasu://overview
watasu://whoami
watasu://teams
watasu://teams/{team}/apps
watasu://apps
watasu://apps/status
watasu://apps/{name}
watasu://apps/{app}/builds
watasu://apps/{app}/builds?limit={limit}
watasu://apps/{app}/builds/latest
watasu://apps/{app}/builds/{number}
watasu://apps/{app}/builds/{number}/logs
watasu://apps/{app}/builds/{number}/logs?limit={limit}
watasu://apps/{app}/builds/{number}/raw-output
watasu://apps/{app}/builds/{number}/raw-output?lines={lines}
watasu://apps/{app}/releases/latest
watasu://apps/{app}/process-types
watasu://apps/{app}/addons
watasu://addons/{name}
```

Discover the server's current resource list rather than fabricating a URI. Start
with `overview`/`whoami`, choose the team, list apps, then inspect the exact app.
Use the resource/template discovery methods your client exposes and follow
returned links. Braces denote placeholders, not literal resource identifiers.
Build selectors are build numbers. Scope visibility can make a resource absent;
absence is not proof the resource does not exist elsewhere.

## Use MCP for

- identifying the authenticated Watasu user and accessible teams;
- finding an app without relying on a local Git remote;
- reading status, current release/build state, process types, and add-on names;
- grounding troubleshooting before suggesting a CLI command;
- confirming post-change read-only state after a user-authorized mutation.

## Do not use MCP for

- fetching or reconstructing secret config;
- making deployments, scaling, access, domain, add-on, or sandbox changes;
- querying application runtime logs when only build/release output resources are
  exposed (these are build logs, not a runtime or arbitrary release-log API);
- inferring billing or permissions that the resource did not return.

If OAuth fails, report the client, requested server URL, consent/team selection,
and sanitized error. Do not ask the user to paste tokens into chat.
For a revoked connection or missing team consent, reconnect through the client's
OAuth flow. For throttling, honor `Retry-After`; see [API errors](api-errors.md).
