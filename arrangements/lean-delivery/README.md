# Lean Delivery

Lean Delivery is a public Codex Multi-Agent V2 arrangement for clearly bounded delivery where the emphasis is a lean role allocation. It uses Luna for ordinary delivery, reserves Sol for read-only integration synthesis and reconciliation, and reserves Astra for critical review. Its main session uses `gpt-5.6-sol` at `high` reasoning effort; each role below is pinned independently.

## Contents

- `config.toml` enables Multi-Agent V2 with the `agents` tool namespace.
- `agents/` contains the 19 role cards.
- `AGENTS.snippet.md` is self-contained orchestration guidance.
- `AGENTS.with-skill.snippet.md` optionally uses `codex-orchestration` and `pragmatic-programmer`, with a standalone fallback.
- `arrangement.toml` describes this arrangement and its optional hook and skills.

Follow the repository [installation guide](../../docs/installation.md) to install an arrangement. This arrangement has no executable dependencies.

## Routing

Classify the task first, then select the least resource-intensive available role that can safely produce the required artifact after checking its current resolved allocation. This arrangement focuses on bounded, established work: all ordinary workers use Luna, `integrator-reviewer` uses Sol only to synthesize and reconcile separate deliveries while remaining read-only, and `critical-reviewer` uses Astra. Among child roles, use at most one active `critical-reviewer` and one active `integrator-reviewer`; all other active children use Luna, while the lead is separate. Escalate when task complexity requires it; the name describes allocation intent, not a measured price or quality claim.

| Role | Model | Reasoning effort |
| --- | --- | --- |
| advisor | gpt-5.6-luna | max |
| backend-worker-light | gpt-5.6-luna | max |
| backend-worker | gpt-5.6-luna | max |
| code-reviewer | gpt-5.6-luna | max |
| critical-reviewer | gpt-6-astra | high |
| database-engineer | gpt-5.6-luna | max |
| debugger | gpt-5.6-luna | max |
| design-lead | gpt-5.6-luna | max |
| docs-writer | gpt-5.6-luna | max |
| explorer | gpt-5.6-luna | max |
| frontend-worker-light | gpt-5.6-luna | max |
| frontend-worker | gpt-5.6-luna | max |
| hard-task-specialist | gpt-5.6-luna | max |
| infra-sre | gpt-5.6-luna | max |
| integrator-reviewer | gpt-5.6-sol | high |
| researcher | gpt-5.6-luna | max |
| security-sweep | gpt-5.6-luna | max |
| test-engineer | gpt-5.6-luna | max |
| test-runner | gpt-5.6-luna | max |

Before spawning, inspect the runtime's live role description and exposed spawn schema; use only a currently available role with its current resolved model and reasoning effort. A running-agent listing is not a role catalog. In a lean installation, return coupling that exceeds the available specialist role to the parent for a stronger available role or a decision. Spawn a selected card with explicit `agent_type` and `fork_turns: "none"`; do not set a model or reasoning effort on the spawn call. Give the child a bounded brief, keep writing assignments non-overlapping, and have the parent inspect every delivery and verify its evidence.

## Capacity

The configuration sets `features.multi_agent_v2.max_concurrent_threads_per_session = 7`: seven total slots including the lead in the target binary's resolved instructions. Use no more than 6 simultaneous children. Live saturation and slot release are separate checks in the [validation record](../../docs/validation.md). Continue independent local work when a spawn is refused.

## Validation status

This catalog makes no claim of completed runtime validation. Validate the installed arrangement against the Codex version named in `arrangement.toml` before relying on it in production work.
