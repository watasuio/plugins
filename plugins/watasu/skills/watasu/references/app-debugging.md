# Application debugging

Debug the first failed lifecycle layer. Do not jump from a browser symptom to a
cluster theory.

## Evidence packet

Record timestamp/time zone, team, app, commit SHA, build and release IDs,
process type, requested hostname, exact sanitized error, and a bounded log
window. Use [MCP](mcp.md) first for current read-only state when available.

## No build

- Confirm repository/remote, branch, and exact commit.
- For GitHub, inspect automatic-deploy setting and required checks on that SHA.
- Confirm a Watasu build was actually created.

## Build failed

- Confirm Dockerfile versus buildpack selection.
- Find the first compiler/image error.
- Check lockfiles, build context, architecture, and public build variables.
- Remember secret and add-on variables do not reach the build.

## Release failed

- Read release output.
- Inspect global or group release command selection.
- Verify required runtime variable names and add-on attachment.
- Establish whether the migration is safe to retry.

## Process unhealthy

- Inspect current formation and bounded runtime logs.
- Check non-root permissions, final command, working directory, shell/entrypoint,
  listener host, and `PORT`.
- For restart loops, identify exit status and the first crash.

## Process healthy, request fails

- HTTP: managed/custom hostname, DNS, TLS, host authorization, app response.
- TCP: exact server process, trust direction, endpoint, protocol credentials.
- RTC: signaling, ephemeral TURN auth, ICE, UDP, media, selected replica.
- Metrics: use the separate [`METRICS_PORT` checklist](metrics.md).

## Add-on failure

Separate provision state, attachment alias, environment-name presence, network,
credentials, logical database/topic/bucket, and client behavior. Never print the
managed connection value.

## Escalate cleanly

If the public surface cannot resolve the problem, provide Watasu support with
sanitized IDs, timestamps, source SHA, failed public operation, and bounded
output. Do not include secrets or speculate about internal infrastructure.

[Handbook](index.md) · [Troubleshooting overview](troubleshooting.md) · [Source map](source-map.md)
