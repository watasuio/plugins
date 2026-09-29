# Sandbox commands, processes, and PTY

Choose the execution surface by interaction model.

## One-shot execution

Use the structured command/code API for bounded, non-interactive work. Capture
execution result, logs, error, and exit status separately. A user-code exception
can be returned inside a successful transport response.

## Streaming processes

The process WebSocket emits start, stdout, stderr, and exit events. Output frames
may be base64 encoded. Persist the cursor so reconnect can replay missed output
without duplicating already-consumed events.

The process API also supports stdin, signals, status/listing, and termination.
Name or retain process IDs when later interaction is expected. In Rust, use the
typed process runner and observe output-cap/truncation metadata.

## PTY

PTY sessions support interactive tools, terminal input, and resize events. Use
them for shells, REPLs, TUIs, debuggers, and installers that truly require a
terminal. Do not parse a colorful terminal stream as if it were stable machine
output when a non-PTY command is available.

## Operational pattern

```text
start bounded command or PTY
record process/session ID
consume stdout/stderr with cursor
send stdin or resize only when expected
wait for final exit/termination event
close transport in finally/defer
leave or stop the underlying sandbox per lifecycle policy
```

An open WebSocket is not proof the process is alive, and a disconnected client
is not proof the process stopped. Reconnect and inspect process state before
starting a duplicate command.

[Handbook](index.md) · [Files](sandbox-files-apply-diff.md) · [Advanced SSH](sandbox-ssh.md)
