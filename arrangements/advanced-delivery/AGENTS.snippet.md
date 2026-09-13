## Multi-Agent V2 orchestration

### Routing

Delegate only a bounded task with an independent result.
Inspect relevant live role descriptions and the current spawn schema; `list_agents` shows the running tree, not a role catalog.
Match an available role and its resolved allocation to read-only discovery, research, decision, or review; a bounded known artifact; unknown-cause diagnosis; coupled invariants; or integration review.
Use the least resource-intensive safe role; do not give edits to a read-only role.

### Dispatch contract

The parent owns selection, integration, validation, and outcome; children never spawn children.
Every spawn explicitly sets `agent_type` and `fork_turns: "none"` and omits call-level model and reasoning-effort overrides.
The brief contains only relevant context, accepted decisions, and any relevant plan; outcome and acceptance criterion; in/out scope and ownership; interfaces and access constraints; expected artifact and checks; and stop conditions plus next consumer.
It needs neither a separate plan document nor a history dump.

### Ownership and evidence

Keep writing ownership non-overlapping; serialize shared files, state, and interacting contracts.
`send_message` only queues a message; `followup_task` starts a completed child on a new turn with its history.
Stop or redirect a child that lacks evidence, exceeds its brief, repeats failure, or conflicts with owned work.
Only the parent integrates, inspects the diff, and verifies responsible checks; skipped, unavailable, or mocked required checks block acceptance.

### Capacity

This fragment configures 6 total session threads, including the parent; use at most 5 simultaneous children.
See [runtime validation](https://github.com/rafaelob/fleet-codex/blob/main/docs/validation.md) for environment-specific verification. A refused spawn does not justify idling while independent local work remains.
