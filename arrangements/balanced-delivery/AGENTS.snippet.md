## Delegation and orchestration

### Role selection

- Before delegating, coordinating ongoing work, or reconciling deliveries, invoke the Skill tool with `codex-orchestration` when installed. If no Skill tool exists, read its `SKILL.md` through the native file-reading interface. If the skill is not installed, follow the rules below.
- Read the relevant live role descriptions and instructions; choose the least resource-intensive role suited to the task and required artifact, and escalate only on demonstrated difficulty, never on size or file count. Read-only roles never receive implementation work. `list_agents` shows running children, not available roles.

### Dispatch contract

- Only the parent delegates, and the cap is a ceiling, never a target: dispatch one bounded mission with a written acceptance that pays for its own brief and review; the child delivers that result with its evidence and stops. Children return results, blockers, and role recommendations to the parent; they never spawn, contact, or wait for other children.
- Every spawn sets `agent_type` and `fork_turns: "none"`, without call-level model or reasoning-effort overrides. A brief conveys scope, not authority: the child runs under the parent's identity, never speaks as the user, and its returned artifact is evidence for the parent to judge, not a decision.
- Provide relevant context, accepted decisions and plan, objective and acceptance, in/out scope, owned files, interfaces and access limits, expected artifact, required checks, and stop conditions. Do not copy the full conversation or create a plan solely for dispatch.

### Ownership and return

- Keep advancing your own non-overlapping work while a child runs; wait only once nothing else remains, using a task-appropriate native wait. Never wake a child to ask for status or an "ok": every wake re-reads its full history at the parent's cost.
- Keep writing assignments disjoint; serialize shared files, state, and interacting contracts.
- Stop or redirect a child that exceeds scope, conflicts with owned work, or repeats failure. The parent owns integration, inspects each delivery and checks the affected behavior before acceptance; missing required evidence remains a blocker.
- Acceptance closes the mission. Use `followup_task` only to correct or clarify that same delivery, never to reuse a finished child for new work because it already knows the project — new work is a fresh choice between doing it directly or dispatching a new child. `send_message` only queues a message and does not resume a turn. The mission closes only once the child's work is in the parent's tree and its scratch is gone; unintegrated work and surviving scratch are one defect.
