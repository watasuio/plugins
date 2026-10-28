# Watasu agent plugins

Official agent integrations for [Watasu](https://watasu.io). The marketplace
currently contains one plugin, `watasu`, with:

- a portable, cross-linked Agent Skill handbook covering customer-side Watasu
  applications, deployments, observability, debugging, and agent sandboxes;
- the Watasu MCP server with read-only access and optional write tools at `https://mcp.watasu.io/mcp`;
- manifests for Claude Code and Codex.

## Let your agent set it up

Paste this into Claude Code, Codex, Cursor, OpenCode, or Pi:

```text
Set up Watasu for me: fetch and follow this guide https://watasu.io/agents.md
```

The [setup guide](https://watasu.io/agents.md) uses the native plugin in Claude Code and Codex,
or the same complete skill handbook and a native MCP connection in Cursor,
OpenCode, and Pi. It explains how to restart and sign in.
The guide's source is maintained in [INSTALL.md](INSTALL.md).

## Claude Code

Install from the public marketplace:

```sh
claude plugin marketplace add watasuio/plugins
claude plugin install watasu@watasu
```

Claude Code starts the MCP server declared by the plugin. Complete the Watasu
OAuth flow when prompted.

## Codex

With a Codex version that supports plugins, run:

```sh
codex plugin marketplace add watasuio/plugins
codex plugin add watasu@watasu
```

The same skill and MCP definition are used by both clients.

Restart the client after installation. Authenticate the
Watasu MCP connection through the client's OAuth flow. Installing the plugin
does not install or authenticate the Watasu CLI: follow the
[CLI setup guide](https://docs.watasu.io/cli/install/), run `watasu login`, then
`watasu whoami` before using CLI operations. MCP tools use the separate MCP connection.

For Homebrew, install the CLI with `brew install watasuio/watasu/watasu`.
The fully qualified name trusts only the Watasu formula; see
[Homebrew tap trust](https://docs.brew.sh/Tap-Trust).

The repository is public; downloading it needs no Watasu organization membership
or private Git access. Using your resources requires your own Watasu account and
team/app permissions. MCP defaults to `read`; request `read write` through your
client’s OAuth flow to enable authorized mutations. Existing read-only grants
stay read-only. The CLI and public sandbox SDK/API remain available. No infrastructure
credentials or platform source checkout are needed.

Start with the [handbook](plugins/watasu/skills/watasu/references/index.md) or
[supported surfaces](plugins/watasu/skills/watasu/references/capabilities.md).
Client setup references: [Claude Code marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
and [Codex plugin packaging](https://developers.openai.com/plugins/build/plugins).

## Development

Run the repository checks before publishing a change:

```sh
python3 scripts/validate.py
claude plugin validate . --strict
claude plugin validate plugins/watasu --strict
```

The skill is intentionally split into a small routing entrypoint and focused
reference chapters. Update the narrowest relevant chapter, keep volatile facts
linked to live Watasu sources, and bump both plugin manifest versions together.
