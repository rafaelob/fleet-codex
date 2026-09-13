## Multi-Agent V2 orchestration

Optional skills can be installed independently. Use the fallback in the relevant section when one is absent; do not invent a callable Skill API on Codex CLI.

### Routing

For dispatch, call the runtime's Skill tool with `codex-orchestration` when exposed; otherwise use its native skill-loading interface to read `SKILL.md`. In Codex prompts, use `$codex-orchestration`.
If it is absent, inspect relevant live role descriptions and the current spawn schema; `list_agents` shows the running tree, not a role catalog.
Match an available role and its resolved allocation to read-only discovery, research, decision, or review; a bounded known artifact; unknown-cause diagnosis; coupled invariants; or integration review.
Use the least resource-intensive safe role; do not give edits to a read-only role.
If the available `hard-task-specialist` cannot safely handle demonstrated coupling, return the choice to the parent.
Among child roles, use at most one active `critical-reviewer` and one active `integrator-reviewer`; all other active children use Luna, while the lead is separate.

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

### Optional engineering guidance

For an ambiguous design or boundary, unexplained green result, duplicate knowledge, contract/input change, reversible-step or spike choice, or shared finite resource, call the Skill tool with `pragmatic-programmer` when exposed; otherwise load its `SKILL.md` natively. In Codex prompts, use `$pragmatic-programmer`.
If it is absent, explain the green signal, name one knowledge authority, validate the boundary and invariants, choose a reversible next step, identify resource ownership and release, and distinguish impossible states from operational errors.

### Capacity

This fragment configures 7 total session threads, including the parent; use at most 6 simultaneous children.
See [runtime validation](https://github.com/rafaelob/fleet-codex/blob/main/docs/validation.md) for environment-specific verification. A refused spawn does not justify idling while independent local work remains.
