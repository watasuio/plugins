# Setup and authentication

Install the CLI using the current [installation guide](https://docs.watasu.io/cli/install/).
Homebrew users can run `brew tap watasuio/watasu` then `brew install watasu`;
other supported platforms have installers in that guide. Verify `watasu
--version` and use command-specific `--help` for the installed version.

## Workstation

```sh
watasu login
watasu whoami
watasu teams
watasu apps --all
```

If the browser cannot open, follow the printed login URL locally. CLI login
stores user-only credentials for the API, Git, and sandbox SSH in `.netrc`
(`_netrc` on Windows). Do not print, attach, or commit that file.

## Headless automation

Create a suitably scoped API key in the customer dashboard and inject it from a
CI secret store. With shell tracing disabled:

```sh
watasu login --api-key "$WATASU_API_KEY"
watasu whoami
```

The variable here supplies the login argument; the CLI uses its credential
store afterwards. SDKs use `WATASU_API_KEY` directly. Never put a literal token
in a command example, a Git remote URL, or a workflow file. Keep jobs and their
credential stores isolated. Use `watasu logout` to remove local CLI credentials;
revoke the API key in the dashboard to invalidate the credential itself.

## MCP is a separate connection

Complete the MCP client's OAuth consent for the intended teams. CLI login does
not sign in MCP, and MCP consent does not sign in Git/CLI. A team-scoped key or
OAuth grant can have narrower visibility than the user's browser session.

On 401/403, check identity, key/consent scope, and app permissions before retrying.
Never use `watasu token` to diagnose authentication: it prints a credential.
Ask the user to authenticate in the client or dashboard, not to paste a key into
chat. Account security settings, passkeys, two-factor authentication, and API-key
revocation belong to the customer's dashboard.

[Handbook](index.md) · [CLI](cli.md) · [MCP](mcp.md) · [Access](teams-access-and-billing.md)
