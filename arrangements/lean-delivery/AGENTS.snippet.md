## Multi-Agent V2 orchestration

### Routing

Delegate only a bounded task with an independent result.
Inspect relevant live role descriptions and the current spawn schema; `list_agents` shows the running tree, not a role catalog.
Match an available role and its resolved allocation to read-only discovery, research, decision, or review; a bounded known artifact; unknown-cause diagnosis; coupled invariants; or integration review.
Use the least resource-intensive safe role; do not give edits to a read-only role.
Luna workers may implement established patterns; model allocation does not change a role's mandate.
Use at most one active `advisor` and one active `integrator-reviewer`; other child roles use Luna. An advisor remains read-only and is not an implementation fallback. If coupling or risk exceeds the available implementing or reviewing role, return to the parent; do not weaken acceptance.

### Responsibilities

Backend/frontend workers handle small edits and write and run their own regression tests. Advisor supplies design direction but never implements. The parent owns documentation, standalone test execution, database and infrastructure work, and coupled or unknown-cause implementation; request separately qualified help when these exceed the parent's scope or capability. Critical-reviewer handles security review; never downgrade the required evidence.

### Dispatch contract

The parent owns selection, integration, validation, and outcome; children never spawn children.
Children return results and blockers only to the parent, never to another child. The parent executes, spawns an available role, or resumes a suitable prior child; a suggested role need not already be active.
Every spawn explicitly sets `agent_type` and `fork_turns: "none"` and omits call-level model and reasoning-effort overrides.
The brief contains only relevant context, accepted decisions, and any relevant plan; outcome and acceptance criterion; in/out scope and ownership; interfaces and access constraints; expected artifact and checks; and stop conditions plus next consumer.
It needs neither a separate plan document nor a history dump.

### Ownership and evidence

Keep writing ownership non-overlapping; serialize shared files, state, and interacting contracts.
`send_message` only queues a message; `followup_task` starts a completed child on a new turn with its history.
Stop or redirect a child that lacks evidence, exceeds its brief, repeats failure, or conflicts with owned work.
Only the parent integrates, inspects the diff, and verifies responsible checks; skipped, unavailable, or mocked required checks block acceptance.

### Capacity

This fragment configures 3 total session threads, including the parent; use at most 2 simultaneous children. Start with one useful child, not a full roster.
See [runtime validation](https://github.com/rafaelob/fleet-codex/blob/main/docs/validation.md) for environment-specific verification. A refused spawn does not justify idling while independent local work remains.
