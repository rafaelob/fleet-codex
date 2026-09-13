## Multi-Agent V2 orchestration

Optional skills can be installed independently. Use the fallback in the relevant section when one is absent; do not invent a callable Skill API on Codex CLI.

### Routing

For dispatch, call the runtime's Skill tool with `codex-orchestration` when exposed; otherwise use its native skill-loading interface to read `SKILL.md`. In Codex prompts, use `$codex-orchestration`.
If it is absent, inspect relevant live role descriptions and the current spawn schema; `list_agents` shows the running tree, not a role catalog.
Match an available role and its resolved allocation to read-only discovery, research, decision, or review; a bounded known artifact; unknown-cause diagnosis; coupled invariants; or integration review.
Use the least resource-intensive safe role; do not give edits to a read-only role.
Luna workers may implement established patterns; model allocation does not change a role's mandate.
Reserve Astra for `advisor` and `hard-task-specialist`, and Sol for `backend-worker` and `integrator-reviewer`. Other roles use Luna, including critical review; if the evidence or available reviewer is insufficient for the risk, return to the parent for an independently qualified review.

### Responsibilities

Regular workers also handle small edits and create their regression tests. Advisor supplies design direction; hard-task-specialist handles unknown-cause diagnosis before a scoped repair. The parent writes documentation; critical-reviewer handles security review. Test-runner runs existing checks and never becomes a test author.

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

### Optional engineering guidance

For an ambiguous design or boundary, unexplained green result, duplicate knowledge, contract/input change, reversible-step or spike choice, or shared finite resource, call the Skill tool with `pragmatic-programmer` when exposed; otherwise load its `SKILL.md` natively. In Codex prompts, use `$pragmatic-programmer`.
If it is absent, explain the green signal, name one knowledge authority, validate the boundary and invariants, choose a reversible next step, identify resource ownership and release, and distinguish impossible states from operational errors.

### Capacity

This fragment configures 4 total session threads, including the parent; use at most 3 simultaneous children. Start with one useful child, not a full roster.
See [runtime validation](https://github.com/rafaelob/fleet-codex/blob/main/docs/validation.md) for environment-specific verification. A refused spawn does not justify idling while independent local work remains.
