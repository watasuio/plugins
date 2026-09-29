# Domains and private networking

Process suffixes determine how a service is reachable. Public HTTP and private
TCP are separate contracts.

## Public HTTP and WebSocket

`web` and `*-web` processes receive managed HTTPS routing. The process listens
on `0.0.0.0:$PORT`; TLS terminates at the managed edge. Application host checks,
WebSocket upgrade handling, cookies, and authentication remain application
responsibilities.

For a custom domain:

1. Add the exact domain to the exact app.
2. Read the DNS target returned by Watasu.
3. Create that record at the customer's DNS provider.
4. Wait for verification and certificate issuance.
5. Validate HTTPS and application host behavior.

Use the current instructions for apex/wildcard records. Never copy a target from
another app or a historical example.

```sh
watasu domains add <hostname> --process <web-process> --app <app>
watasu domains info <hostname> --app <app>
watasu domains wait <hostname> --app <app>
```

Quote wildcard hostnames so the local shell does not expand them. Follow every
returned DNS instruction, including verification/delegation records when present.
If pending, inspect the exact domain state and public DNS before changing records
again. Customer DNS changes happen at the customer's DNS provider; platform TLS
and routing remain managed by Watasu.

## Private TCP

A process ending in `-tcp` exposes raw TCP only to explicitly trusted sibling
apps. It listens on `$PORT` and trusted callers use the Watasu-provided internal
hostname documented for the exact app/process.

The server app owns a directional trust list:

```sh
watasu apps:trust --app <server-app>
watasu apps:trust <client-app> --app <server-app>
watasu apps:trust --clear --app <server-app>
```

Confirm current CLI help before mutation. If app A is trusted by app B, A can
reach B's private service; the reverse is not implied. Cross-team private reach
is not part of this contract.
Inspect the current list before setting it: supply the intended complete list of
trusted siblings, preserving existing grants unless their removal is authorized.

Trust grants network reachability, not caller identity. Keep mTLS, signed tokens,
or protocol credentials for sensitive services.

## Diagnosis

- Public: process health, managed hostname, custom-domain state, DNS, TLS,
  application host/routing.
- Private: exact process suffix, server listener, trust direction, internal
  endpoint, protocol auth.

Calling a public Watasu hostname from another app uses the public route and does
not require private trust.

[Handbook](index.md) · [Processes](processes-networking-and-domains.md) · [RTC](rtc.md)
