# Balanced Delivery

Everyday product delivery with Luna implementing established patterns, Sol handling backend work and integration review, and Astra handling decisions and coupled implementation. The lead uses `gpt-5.6-sol` at `xhigh`. This is an allocation policy, not a measured quality or cost guarantee.

## Install

Follow the [installation guide](../../docs/installation.md). Merge only `config.toml`, install the 12 `agents/*.toml` cards, and insert either `AGENTS.snippet.md` or the optional-skill variant. The manifest references independent, optional skills and a hook; none is automatically enabled. No private tools or configuration are required.

## Routing

Read the live role's description, instructions, resolved model and effort before dispatch. Match the artifact and task difficulty, not the role name alone. Luna is an implementation model for established patterns, not just a reconnaissance option. Keep implementation, advice, and independent review separate.

Reserve Astra for `advisor` and `hard-task-specialist`, and Sol for `backend-worker` and `integrator-reviewer`. Other roles use Luna, including critical review; if the evidence or available reviewer is insufficient for the risk, return to the parent for an independently qualified review.

| Role | Model | Reasoning effort |
| --- | --- | --- |
| advisor | gpt-6-astra | high |
| backend-worker | gpt-5.6-sol | high |
| code-reviewer | gpt-5.6-luna | max |
| critical-reviewer | gpt-5.6-luna | max |
| database-engineer | gpt-5.6-luna | max |
| explorer | gpt-5.6-luna | max |
| frontend-worker | gpt-5.6-luna | max |
| hard-task-specialist | gpt-6-astra | high |
| infra-sre | gpt-5.6-luna | max |
| integrator-reviewer | gpt-5.6-sol | high |
| researcher | gpt-5.6-luna | max |
| test-runner | gpt-5.6-luna | max |

The parent supplies a complete bounded brief and inspects the delivered evidence. Every spawn uses `agent_type` and `fork_turns: "none"`, with no call-level model or effort override. Children never spawn children.

## Capacity and simplicity

The V2 fragment sets **4 total threads including the lead**, allowing **at most 3 simultaneous children** in the target runtime. Start with one useful delegation and add another only for a disjoint result. Reconcile an implementation batch before starting another; do not fill the cap by routine.

The 12 role cards are available responsibilities, not 12 running agents. Removed roles have explicit owners:

Regular workers also handle small edits and create their regression tests. Advisor supplies design direction; hard-task-specialist handles unknown-cause diagnosis before a scoped repair. The parent writes documentation; critical-reviewer handles security review. Test-runner runs existing checks and never becomes a test author.

This is an adapted public roster, not a full personal-profile export. Retained roles preserve the task-based model allocation. Conservative caps are design choices, not benchmark-derived optima; see [the rationale](../../docs/orchestration.md).

## Validation status

Revision 0.2.0 changes allocations and caps. Historical native tests from 0.1.0 do not certify this revision. Full live role coverage, concurrency saturation, and slot release remain unverified; see [the validation record](../../docs/validation.md). Installation still requires account/model availability and compatible runtime checks.
