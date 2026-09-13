# Advanced Delivery

Advanced Delivery is a public Codex Multi-Agent V2 arrangement for work whose delivery complexity warrants a specialist role map: coupled invariants, cross-component changes, independent review, and investigation with conflicting evidence. Its main session uses `gpt-5.6-sol` at `xhigh` reasoning effort; each role below is pinned independently.

## Contents

- `config.toml` enables Multi-Agent V2 with the `agents` tool namespace.
- `agents/` contains the 19 role cards.
- `AGENTS.snippet.md` is self-contained orchestration guidance.
- `AGENTS.with-skill.snippet.md` optionally uses `codex-orchestration` and `pragmatic-programmer`, with a standalone fallback.
- `arrangement.toml` describes this arrangement and its optional hook and skills.

Follow the repository [installation guide](../../docs/installation.md) to install an arrangement. This arrangement has no executable dependencies.

## Routing

Classify the task first, then select the least resource-intensive available role that can safely produce the required artifact after checking its current resolved allocation. This arrangement prioritizes delivery complexity over a lean allocation: light workers handle fully specified small edits, ordinary workers handle bounded work on established patterns, and specialist roles are reserved for coupled invariants, unknown causes, and independent review. It makes no measured price or quality claim.

| Role | Model | Reasoning effort |
| --- | --- | --- |
| advisor | gpt-6-astra | high |
| backend-worker-light | gpt-5.6-luna | max |
| backend-worker | gpt-5.6-terra | max |
| code-reviewer | gpt-5.6-terra | max |
| critical-reviewer | gpt-6-astra | high |
| database-engineer | gpt-5.6-terra | max |
| debugger | gpt-5.6-terra | max |
| design-lead | gpt-6-astra | high |
| docs-writer | gpt-5.6-luna | max |
| explorer | gpt-5.6-luna | max |
| frontend-worker-light | gpt-5.6-luna | max |
| frontend-worker | gpt-5.6-terra | max |
| hard-task-specialist | gpt-6-astra | high |
| infra-sre | gpt-5.6-terra | max |
| integrator-reviewer | gpt-5.6-terra | max |
| researcher | gpt-5.6-luna | max |
| security-sweep | gpt-5.6-terra | max |
| test-engineer | gpt-5.6-terra | max |
| test-runner | gpt-5.6-luna | max |

Before spawning, inspect the runtime's live role description and exposed spawn schema; use only a currently available role with its current resolved model and reasoning effort. A running-agent listing is not a role catalog. Spawn a selected card with explicit `agent_type` and `fork_turns: "none"`; do not set a model or reasoning effort on the spawn call. Give the child a bounded brief, keep writing assignments non-overlapping, and have the parent inspect every delivery and verify its evidence.

## Capacity

The configuration sets `features.multi_agent_v2.max_concurrent_threads_per_session = 6`: six total slots including the lead in the target binary's resolved instructions. Use no more than 5 simultaneous children. Live saturation and slot release are separate checks in the [validation record](../../docs/validation.md). Continue independent local work when a spawn is refused.

## Validation status

This catalog makes no claim of completed runtime validation. Validate the installed arrangement against the Codex version named in `arrangement.toml` before relying on it in production work.
