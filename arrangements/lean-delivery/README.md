# Lean Delivery

Cost-conscious, well-bounded delivery with Luna implementing and reviewing, Sol reconciling deliveries, and one Astra advisor for decisions. The lead uses `gpt-5.6-sol` at `high`. This is an allocation policy, not a measured quality or cost guarantee.

## Install

Follow the [installation guide](../../docs/installation.md). Merge only `config.toml`, install the 8 `agents/*.toml` cards, and insert either `AGENTS.snippet.md` or the optional-skill variant. The manifest references independent, optional skills and a hook; none is automatically enabled. No private tools or configuration are required.

## Routing

Read the live role's description, instructions, resolved model and effort before dispatch. Match the artifact and task difficulty, not the role name alone. Luna is an implementation model for established patterns, not just a reconnaissance option. Keep implementation, advice, and independent review separate.

Use at most one active `advisor` and one active `integrator-reviewer`; other child roles use Luna. An advisor remains read-only and is not an implementation fallback. Coupled and unknown-cause implementation belongs to the parent. If risk exceeds the available reviewer, obtain independently qualified review; do not weaken acceptance.

| Role | Model | Reasoning effort |
| --- | --- | --- |
| advisor | gpt-6-astra | high |
| backend-worker | gpt-5.6-luna | max |
| code-reviewer | gpt-5.6-luna | max |
| critical-reviewer | gpt-5.6-luna | max |
| explorer | gpt-5.6-luna | max |
| frontend-worker | gpt-5.6-luna | max |
| integrator-reviewer | gpt-5.6-sol | high |
| researcher | gpt-5.6-luna | max |

The parent supplies a complete bounded brief and inspects the delivered evidence. Every spawn uses `agent_type` and `fork_turns: "none"`, with no call-level model or effort override. Children never spawn children.

## Capacity and simplicity

The V2 fragment sets **3 total threads including the lead**, allowing **at most 2 simultaneous children** in the target runtime. Start with one useful delegation and add another only for a disjoint result. Reconcile an implementation batch before starting another; do not fill the cap by routine.

The 8 role cards are available responsibilities, not 8 running agents. Removed roles have explicit owners:

Backend/frontend workers handle small edits and write and run their own regression tests. Advisor supplies design direction but never implements. The parent owns documentation, standalone test execution, database and infrastructure work, and coupled or unknown-cause implementation; request separately qualified help when these exceed the parent's scope or capability. Critical-reviewer handles security review; never downgrade the required evidence.

This is an adapted public roster, not a full personal-profile export. Retained roles preserve the task-based model allocation. Conservative caps are design choices, not benchmark-derived optima; see [the rationale](../../docs/orchestration.md).

## Validation status

Revision 0.4.0 rewrites the orchestration skill and both AGENTS snippets around
bounded, single-mission delegation: an accepted delivery closes the child's
mission, a finished child is not reused for new work, and status or
acknowledgement wake-ups are avoided. This roster and cap are unchanged. See
[upgrade instructions](../../docs/installation.md#upgrading-from-03x).

Revision 0.3.0 adds a one-minute minimum and five-minute default for native child
waits, without changing this roster or cap. Choose explicit waits according to
the task; see [adaptive waiting](../../docs/orchestration.md#adaptive-waiting)
and [upgrade instructions](../../docs/installation.md#upgrading-from-02x).
Configuration checks are not measurements of quota savings or waiting behavior.

Revision 0.2.0 changes allocations and caps. Historical native tests from 0.1.0 do not certify this revision. Full live role coverage, concurrency saturation, and slot release remain unverified; see [the validation record](../../docs/validation.md). Installation still requires account/model availability and compatible runtime checks.
