# Sandbox pause, checkpoints, and storage

Pause, checkpoint, and volume solve different persistence problems.

| Mechanism | Preserves | Resume/restore behavior |
| --- | --- | --- |
| Pause | Whole-machine memory/process state when available, plus disk | Same sandbox ID; may fall back to disk restart after platform changes |
| Checkpoint | Disk state only | Restore creates a new sandbox |
| Volume | Named team-scoped persistent filesystem | Mount into sandboxes; independent lifecycle |

## Pause and resume

Use pause when a developer or agent should reconnect to the same environment.
Do not promise that in-memory processes survive every upgrade: the documented
fallback restarts from retained disk while keeping the sandbox identity.

## Checkpoints

Choose `guest` consistency when the guest can quiesce filesystems and `crash`
consistency when a crash-consistent disk capture is acceptable. Set an expiry
deliberately. List and paginate checkpoints globally when auditing retained
storage.

Restore keeps relevant class/template/network/ports/metadata but creates a new
sandbox. Validate the new machine before destroying the source.

## Volumes

Volumes support detached read/write/list/directory/path operations. Conflicting
writes or destructive operations can be refused while a volume is attached to a
live sandbox. Resolve attachment state rather than bypassing the safety guard.

## Lifecycle and billing

Paused machine images, retained sandbox disk, checkpoints, template versions,
and volumes can each contribute storage usage. Runtime and requested resources
are separate dimensions. Read live limits/pricing before estimating costs, set
timeouts/expiries, and never delete retained state without explicit intent.

[Handbook](index.md) · [Lifecycle](sandbox-lifecycle.md) · [Sandbox debugging](sandbox-debugging.md)
