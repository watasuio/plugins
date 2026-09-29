# Advanced sandbox SSH

SSH provides shell-native development on Watasu sandboxes. The host is always:

```text
box.watasu.io
```

## Username grammar

```text
base                         default base template
base:<version-or-id-or-tag>  selected base version
team/base                    team-scoped template
s-6231                       reconnect to sandbox by ID
ls                           list available/recent targets
```

Examples:

```sh
ssh base@box.watasu.io
ssh -t team/base@box.watasu.io
ssh s-6231@box.watasu.io
ssh base@box.watasu.io -- npm test
printf '%s\n' input | ssh base@box.watasu.io -- ./processor
```

One-off commands propagate their exit code and can stream stdin/stdout. Use
`-t` for shells, REPLs, TUIs, and other terminal-aware programs.

## Connection options with `SetEnv`

Supported options include `WATASU_TEAM`, `WATASU_TIMEOUT`,
`WATASU_ON_TIMEOUT`, `WATASU_CPU`, `WATASU_MEMORY`, `WATASU_REGION`,
`WATASU_SNAPSHOT`, `WATASU_USER`, `WATASU_WORKDIR`, `WATASU_QUIET`, and
`WATASU_NO_ENROLL`. Unknown `WATASU_*` options fail instead of being ignored.

Use your SSH client's `SetEnv` syntax and verify the current SSH docs for value
formats. Do not place tokens in SSH config files shared with others.

## Authentication and host identity

The initial supported token flow can enroll the offered SSH public key, with a
bounded number of automatically enrolled keys. Set `WATASU_NO_ENROLL=1` when
one-time authentication must not register the key. Verify the current documented
host-key fingerprint or SSHFP record before trusting a first connection.

## Persistence semantics

The default SSH sandbox has a bounded deadline and pauses on timeout. `exit`
pauses it immediately; a dropped network connection can leave it running until
the deadline. Reconnection attaches to the same sandbox and can replay recent
scrollback. Multiple sessions may share one sandbox, so inspect before assuming
exclusive control.

## Deliberate limitations

SSH does not imply `scp`, SFTP, port forwarding, agent forwarding, or X11. Use
the file APIs/signed URLs for transfer and explicit public previews for HTTP.

[Handbook](index.md) · [Processes and PTY](sandbox-processes-pty.md) · [Networking](sandbox-networking.md)
