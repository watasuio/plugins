# Set up Watasu for your agent

Set up Watasu skills and the hosted MCP connection from
[`watasuio/plugins`](https://github.com/watasuio/plugins). Use **only the section
for the agent running this conversation**: Claude Code, Codex, Cursor, OpenCode,
or Pi. Reuse matching installations and preserve unrelated settings and skills.
For another client, explain that this guide does not yet cover it.

## Claude Code

Check `claude plugin list` first. If `watasu@watasu` is already installed, skip
installation. Otherwise run:

```sh
claude plugin marketplace add watasuio/plugins
claude plugin install watasu@watasu
```

Verify with `claude plugin list`. If the plugin is installed but disabled,
enable it with `claude plugin enable watasu@watasu`.

## Codex

Check `codex plugin list` first. If `watasu@watasu` is already installed, skip
installation. Otherwise run:

```sh
codex plugin marketplace add watasuio/plugins
codex plugin add watasu@watasu
```

Verify that Watasu is installed and enabled with `codex plugin list`. If it is
disabled, ask the user to enable Watasu in Plugins; in Codex CLI, open `/plugins`,
select Watasu, and press Space to enable it. If `codex plugin` is unavailable,
tell the user to update Codex to a version with plugin support and retry.
Do not substitute a manual skill copy or a separate MCP installation.

## Cursor, OpenCode, and Pi: install the skill

These clients load the same handbook through their native Agent Skills support.
Clone `https://github.com/watasuio/plugins.git` into a temporary directory.
Copy the **whole** `plugins/watasu/skills/watasu` directory, including
`references/`, into the location for your current client:

| Client | Skill destination |
| --- | --- |
| Cursor | `~/.cursor/skills/watasu/` |
| OpenCode | `~/.config/opencode/skills/watasu/` |
| Pi | `~/.pi/agent/skills/watasu/` |

Use the client's configured directory if customized (for Pi, `PI_CODING_AGENT_DIR`
replaces `~/.pi/agent`). Verify that `SKILL.md` and `references/index.md` are
present. Copying only `SKILL.md` loses the handbook. Then connect MCP below.

### Cursor

Merge this entry into `~/.cursor/mcp.json`, preserving other servers:

```json
{
  "mcpServers": {
    "watasu": { "url": "https://mcp.watasu.io/mcp" }
  }
}
```

After restarting, ask the user to sign in to the Watasu MCP server in Cursor's
Customize panel. Confirm the Watasu skill and enabled server appear there.

### OpenCode

Merge this entry into the user's OpenCode config (normally
`~/.config/opencode/opencode.json` or its existing `.jsonc` equivalent):

```json
{
  "mcp": {
    "watasu": {
      "type": "remote",
      "url": "https://mcp.watasu.io/mcp",
      "enabled": true
    }
  }
}
```

Ask the user to run `opencode mcp auth watasu` and complete browser sign-in.
Verify with `opencode mcp list` and, after restarting, the native `skill` tool's
Watasu entry.

### Pi

Check `pi mcp list` first. If Watasu is not configured, run:

```sh
pi mcp add watasu --url https://mcp.watasu.io/mcp
```

Ask the user to run `pi mcp login watasu` and complete browser sign-in. Verify
with `pi mcp list` and, after restarting, `/skill:watasu`. If `pi mcp` is
unavailable, ask the user to update Pi; no MCP adapter is needed.

## Finish

Report whether installation succeeded and tell the user:

> Restart your agent to load Watasu, then sign in to Watasu when the
> MCP connection asks you to authenticate.

For desktop apps such as Codex and Cursor, fully quit and reopen the app.

In Claude Code, the user can open `/mcp` to sign in to Watasu. In Codex, use the
Watasu connection's sign-in action. OAuth sign-in requires the user; never ask
them to paste a password or token into the conversation. Do not claim the MCP
connection is working until authentication and a read-only Watasu request have
succeeded. If setup failed, report the specific error and next action instead
of claiming success.

Claude Code and Codex plugins configure MCP themselves; do not add a second
server for them. Installing or signing in to the Watasu CLI is a separate step,
needed only when a later task calls for it. This setup does not deploy or change
any Watasu resources.

If that later task needs the CLI, Homebrew users can run:

```sh
brew install watasuio/watasu/watasu
```

This installs and trusts only the Watasu formula. For other platforms or an
existing install that reports a trust error, follow the
[CLI installation guide](https://docs.watasu.io/cli/install/).

Official client references:
[Claude Code](https://code.claude.com/docs/en/plugin-marketplaces),
[Codex](https://learn.chatgpt.com/docs/developer-commands#codex-plugin),
[Cursor skills](https://cursor.com/docs/skills) and [MCP](https://cursor.com/docs/mcp),
[OpenCode skills](https://opencode.ai/docs/skills/) and [MCP](https://opencode.ai/docs/mcp-servers/),
[Pi skills](https://pi.dev/docs/latest/skills) and [MCP](https://pi.dev/docs/latest/mcp).
