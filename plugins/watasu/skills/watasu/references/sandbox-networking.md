# Sandbox networking and previews

Start with the narrowest network policy. Watasu can control internet access,
package-registry access, public traffic, allowed outbound destinations, denied
destinations, and reusable egress profiles.

## Create and live updates

Set initial network policy during create. A live policy update through the
supported `PUT` persists desired state; Watasu retries application when needed.
Do not replace a narrow policy with unrestricted internet merely to diagnose one
hostname.

Separate these questions:

1. Does DNS resolve inside the sandbox?
2. Does network policy allow the destination/port?
3. Is the remote service reachable?
4. Does application TLS/authentication succeed?

## Public HTTP previews

A preview needs both:

- `allow_public_traffic`; and
- an exposed port declared as public HTTP.

The process must listen on the exposed port, preferably `0.0.0.0`. The preview
shape is:

```text
https://p<port>-<route-token>.sandbox.watasuhost.com
```

Treat the route token and full URL as a shareable capability. Do not publish it
accidentally. A preview route does not add application authentication.

## Diagnose a preview

- sandbox is running and the session is current;
- public traffic is allowed;
- exact port is declared HTTP/public;
- process is listening on `0.0.0.0:<port>`;
- URL belongs to the current route token;
- application accepts the preview host and protocol;
- logs show the incoming request.

SSH port forwarding is not supported; use an explicit preview or supported
data-plane connection.

[Handbook](index.md) · [Lifecycle](sandbox-lifecycle.md) · [Advanced SSH](sandbox-ssh.md)
