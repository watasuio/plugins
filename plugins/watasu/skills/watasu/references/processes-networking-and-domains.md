# Processes, networking, and domains

See [`PORT`, health, and startup](ports-health-and-startup.md) for listener
behavior, [release commands](release-commands-and-migrations.md) for gates,
[domains and private networking](domains-and-private-networking.md) for routing,
and [RTC](rtc.md) for TURN/media details.

## Process naming contract

Procfile names carry routing and release semantics:

| Name | Behavior |
| --- | --- |
| `web` or `*-web` | Public HTTP/TLS service |
| `*-tcp` | Private TCP service with explicit directional trust |
| `*-rtc` | Realtime service with TURN/UDP support and per-replica hostnames |
| `release` | Command that gates the entire release |
| `<group>-release` | Command that gates process types sharing that group prefix |
| Any other name | Non-routed/background process |

Choose names intentionally. Renaming a process can change its routing or release
role, not merely its label.

## Release commands

Use `release` for migrations or other work that must succeed before the entire
release becomes current. Use a group release command only when the gate belongs
to that process group. Commands must be repeatable or safely recoverable because
deploy retries can happen.

On failure, inspect release output and leave the prior healthy release serving.
Do not work around a failed release command by manually changing database state
unless the user explicitly authorizes the exact recovery.

## Public HTTP and custom domains

Web processes receive a managed `*.watasuhost.com` hostname. The application
must bind to `0.0.0.0:$PORT` and answer on the routed port.

Custom domains apply to web processes. The normal flow is:

1. Add the exact domain to the app.
2. Read the DNS target Watasu returns.
3. Add the required DNS record at the customer's DNS provider.
4. Wait for DNS verification and certificate issuance.
5. Validate HTTPS and the expected host in the application.

Handle apex and wildcard records according to the current domain instructions.
Do not guess a target from another app or hardcode a historical endpoint.

## Private TCP

TCP process types are private. Connectivity requires an explicit directional
trust relationship from the client app/process to the server app/process. Trust
controls reachability, not application authentication; keep protocol-level
credentials and authorization.

When diagnosing TCP:

- verify both exact process names;
- verify trust direction;
- verify the server listens on the provided address/port;
- verify the client uses the Watasu-provided private endpoint;
- separate network reachability from protocol authentication.

## RTC

RTC process types receive Watasu TURN configuration and per-replica routing
information. Use the provided environment variables; do not invent TURN
credentials or static node addresses. Reconcile application-level signaling,
ICE configuration, UDP reachability, and replica-specific hostnames separately.

Do not confuse application `PORT`, public `TURN_PORT`, media candidates, and
observability-only `METRICS_PORT`.

## Process inspection

Use MCP or `watasu ps --app <app>` for current formation and process state. Use
runtime logs for crashes/readiness failures, releases for rollout state, and
domain state for DNS/TLS. A healthy process alone does not prove that a custom
domain, TCP trust, or RTC path works.

[Handbook](index.md) · [Domains and private networking](domains-and-private-networking.md) · [RTC](rtc.md)
