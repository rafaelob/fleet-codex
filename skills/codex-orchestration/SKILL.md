---
name: codex-orchestration
description: "Route bounded Codex subagent work from live role availability, use the V2 spawn contract, and reconcile independent deliveries."
license: Apache-2.0
---

# Codex Orchestration

Use this procedure when a task is independently useful enough to delegate. The parent owns task selection, integration, validation, and the final outcome. A child never spawns another child, even if a child interface is visible to it.

## Classify before dispatch

Identify the requested artifact, whether it needs reading, implementation, testing, review, research, diagnosis, or integration, and the consequence of a wrong result. Do not delegate a one-file search or a simple edit when direct work is cheaper than rebuilding context in a child.

Before dispatch, inspect only the relevant live role descriptions and exposed spawn schema. Use only role identifiers the current runtime exposes, and check the selected role's current resolved model and reasoning effort. Live descriptions are the authority; `list_agents` reports the running agent tree, not a role catalog.

Match the task type to a currently available role: use a read-only specialist for discovery, primary-source research, decisions, or independent review; an implementing role for a bounded known artifact; a test specialist for a coverage or named-suite need; a debugger for an unknown cause; a stronger specialist for coupled invariants; and an integration reviewer to synthesize separate deliveries against one contract. These are routing examples, not a static role catalog.

Select the least resource-intensive available role that can safely deliver the artifact. Do not assume a universal cost or capability order from role names or model labels. Use a light worker only when behavior, files, validation, and ownership are already clear. If demonstrated coupling or risk exceeds an available role, return the choice to the parent for a stronger available role or a decision. A read-only role assigned a write task must report the mismatch and stop.

## Spawn contract

Use the runtime's native subagent interface and its current schema. Set the selected identifier explicitly in `agent_type` and always pass `fork_turns: "none"`. Do not provide model or reasoning-effort overrides on the spawn call: the selected role card owns them. Put the relevant context in the child brief rather than passing a long inherited conversation.

Every brief must include:

1. Only relevant context, accepted decisions, and any relevant plan; do not attach full history or create a plan just to dispatch.
2. Objective and testable acceptance criterion.
3. In-scope and out-of-scope work, ownership, known existing work, and possible overlap.
4. Interfaces and access constraints.
5. Expected artifact and checks to run.
6. Stop condition, escalation path, and next consumer.

Use an action verb that matches the needed result: inspect, implement, test, review, or research. Ask for a diff when a diff is wanted; ask for a report when the child must remain read-only.

## Child lifecycle and capacity

`send_message` queues a message for an existing child but does not start or resume its turn. Use `followup_task` to give a completed child a new turn while preserving its history.

Respect the chosen arrangement's allocation, per-role limits, and configured cap, then confirm the current runtime's resolved limits. A refused spawn is not a reason to idle: continue independent local work and wait only when nothing remains to advance.

## Coordinate and accept

Give writing children non-overlapping file or component ownership. Serialize work that shares a file, mutable state, or an interacting contract. Stop or redirect a child that lacks evidence, exceeds its brief, repeats failure, or conflicts with owned work. Only the parent integrates deliveries. If two independent deliveries must combine, use an available integration reviewer before the parent accepts the combined result. High-risk work still needs the independent critical review appropriate to its risk.

An implementing child should complete the requested artifact and affected checks before handoff, rather than return a first draft. Safe local work and disposable-fixture checks may continue within the brief; production side effects remain outside child scope. Repeat a check only after a relevant change or new evidence.

The parent must read the actual diff, verify reported commands and results, and validate the affected behavior at the responsible layer. A skipped, unavailable, empty, or mocked-away required check is a blocker, not a pass. Correct in-scope defects and rerun the affected checks before completion.
