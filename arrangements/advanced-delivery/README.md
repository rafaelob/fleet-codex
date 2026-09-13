# Advanced Delivery

Complex product delivery with dedicated reasoning for decisions, diagnosis, ordinary review, critical review, and coupled implementation. The lead uses `gpt-5.6-sol` at `xhigh`. This is an allocation policy, not a measured quality or cost guarantee.

## Install

Follow the [installation guide](../../docs/installation.md). Merge only `config.toml`, install the 15 `agents/*.toml` cards, and insert either `AGENTS.snippet.md` or the optional-skill variant. The manifest references independent, optional skills and a hook; none is automatically enabled. No private tools or configuration are required.

## Routing

Read the live role's description, instructions, resolved model and effort before dispatch. Match the artifact and task difficulty, not the role name alone. Luna is an implementation model for established patterns, not just a reconnaissance option. Keep implementation, advice, and independent review separate.

Reserve Sol for backend implementation, unknown-cause diagnosis, ordinary review, and integration review; reserve Astra for advice, design direction, coupled implementation, and critical review.

| Role | Model | Reasoning effort |
| --- | --- | --- |
| advisor | gpt-6-astra | high |
| backend-worker | gpt-5.6-sol | high |
| code-reviewer | gpt-5.6-sol | high |
| critical-reviewer | gpt-6-astra | high |
| database-engineer | gpt-5.6-luna | max |
| debugger | gpt-5.6-sol | high |
| design-lead | gpt-6-astra | high |
| explorer | gpt-5.6-luna | max |
| frontend-worker | gpt-5.6-luna | max |
| hard-task-specialist | gpt-6-astra | high |
| infra-sre | gpt-5.6-luna | max |
| integrator-reviewer | gpt-5.6-sol | high |
| researcher | gpt-5.6-luna | max |
| test-engineer | gpt-5.6-luna | max |
| test-runner | gpt-5.6-luna | max |

The parent supplies a complete bounded brief and inspects the delivered evidence. Every spawn uses `agent_type` and `fork_turns: "none"`, with no call-level model or effort override. Children never spawn children.

## Capacity and simplicity

The V2 fragment sets **5 total threads including the lead**, allowing **at most 4 simultaneous children** in the target runtime. Start with one useful delegation and add another only for a disjoint result. Reconcile an implementation batch before starting another; do not fill the cap by routine.

The 15 role cards are available responsibilities, not 15 running agents. Removed roles have explicit owners:

Regular backend/frontend workers also handle fully specified small edits. The parent writes documentation; critical-reviewer handles scoped security review. Light variants and a separate security sweep are omitted.

This is an adapted public roster, not a full personal-profile export. Retained roles preserve the task-based model allocation. Conservative caps are design choices, not benchmark-derived optima; see [the rationale](../../docs/orchestration.md).

## Validation status

Revision 0.3.0 adds a one-minute minimum and five-minute default for native child
waits, without changing this roster or cap. Choose explicit waits according to
the task; see [adaptive waiting](../../docs/orchestration.md#adaptive-waiting)
and [upgrade instructions](../../docs/installation.md#upgrading-from-02x).
Configuration checks are not measurements of quota savings or waiting behavior.

Revision 0.2.0 changes allocations and caps. Historical native tests from 0.1.0 do not certify this revision. Full live role coverage, concurrency saturation, and slot release remain unverified; see [the validation record](../../docs/validation.md). Installation still requires account/model availability and compatible runtime checks.
