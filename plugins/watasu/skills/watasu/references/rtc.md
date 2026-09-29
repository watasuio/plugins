# RTC and TURN

An `*-rtc` process is for realtime media workloads such as an SFU. Watasu
provides network primitives—TURN access and per-replica addresses—but the
application still owns signaling, sessions, authorization, and media behavior.

## Variables

RTC processes can receive:

```text
TURN_URL
TURN_HOST
TURN_PORT
TURN_TRANSPORT
TURN_REALM
TURN_AUTH_TYPE
TURN_SHARED_SECRET
TURN_TTL_SECONDS
WATASU_RTC_BASE_HOST
WATASU_RTC_BASE_LABEL
WATASU_RTC_BASE_DOMAIN
WATASU_RTC_INSTANCE_ORDINAL
WATASU_RTC_INSTANCE_INDEX_WIDTH
```

Treat all as platform-owned. Read them at runtime and never expose
`TURN_SHARED_SECRET` to browsers, logs, or client bundles.

## Responsibility split

- A web/signaling process authenticates the user, allocates a media replica, and
  returns short-lived ICE/TURN credentials.
- The RTC process terminates or forwards realtime media.
- Watasu supplies TURN/UDP reachability and deterministic replica identity.
- The client performs ICE using the application-provided short-lived settings.

Generate ephemeral credentials server-side using a current TURN REST-compatible
library and the injected authentication mode, secret, realm, and TTL. Do not
invent static credentials or freeze a credential algorithm when the documented
gateway contract can change.

## Replica addressing

Build the selected replica hostname from the injected base label/domain,
ordinal, and index width. For ordinal `0` and width `2`, the visible suffix is
`01`. Keep a media session on the chosen replica; do not randomly load-balance
packets for one session across replicas.

## Three ports that are easy to confuse

- `PORT`: service/probe listener inside the RTC application container.
- `TURN_PORT`: public TURN gateway port used by clients.
- Media/ICE candidates: addresses negotiated by the RTC stack for media.

They are not interchangeable. `METRICS_PORT`, when present, is a fourth,
observability-only listener.

## Debug in layers

1. Signaling: session allocation and replica selection.
2. ICE gathering: client has usable host/server-reflexive/relay candidates.
3. TURN auth: credentials are fresh, correctly scoped, and not leaked.
4. Connectivity: UDP/TURN path succeeds from the affected network.
5. Media: codecs, DTLS/SRTP, RTP/RTCP, and SFU state.
6. Replica: logs and metrics match the hostname allocated to the session.

Use `watasu logs --app <app> --process-type <name-rtc>` and process inspection.
A successful WebSocket/signaling connection does not prove media connectivity.

[Handbook](index.md) · [Processes](processes-networking-and-domains.md) · [Ports](ports-health-and-startup.md)
