## Delegation and orchestration

### Role selection

- Before delegating, coordinating ongoing work, or reconciling deliveries, invoke the Skill tool with `codex-orchestration` when installed. If no Skill tool exists, read its `SKILL.md` through the native file-reading interface. If the skill is not installed, follow the rules below.
- Read the relevant live role descriptions and instructions; choose the least resource-intensive role suited to the task and required artifact. Read-only roles never receive implementation work. `list_agents` shows running children, not available roles.

### Dispatch contract

- Only the parent delegates. Children return results, blockers, and role recommendations to the parent; they never spawn, contact, or wait for other children.
- Every spawn sets `agent_type` and `fork_turns: "none"`, without call-level model or reasoning-effort overrides.
- Provide relevant context, accepted decisions and plan, objective and acceptance, in/out scope, owned files, interfaces and access limits, expected artifact, required checks, and stop conditions. Do not copy the full conversation or create a plan solely for dispatch.

### Ownership and return

- When only delegated work remains, use task-appropriate native waits; avoid repeated status polling.
- Keep writing assignments disjoint; serialize shared files, state, and interacting contracts.
- Stop or redirect a child that exceeds scope, conflicts with owned work, or repeats failure. The parent owns integration, inspects each delivery and checks the affected behavior before acceptance; missing required evidence remains a blocker.
- Use `followup_task` to resume a suitable completed child; `send_message` only queues a message. A recommended role need not already be running.
