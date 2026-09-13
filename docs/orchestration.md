# Why these orchestration choices

These arrangements package a delegation policy, not a replacement for your
AGENTS.md or personal Codex configuration. Insert only the suggested section and
merge only the supplied TOML fields. Keep the longer explanations in this guide
instead of loading them into every conversation.

## Choose by complexity and cost intent

**Advanced Delivery** assigns more capable specialist models to difficult design,
advice, coupled implementation and critical review. Use it when uncertainty and
business impact justify more reasoning across several responsibilities.

**Balanced Delivery** is the middle ground for everyday product delivery: Astra
handles advice and coupled implementation; Sol handles backend implementation and
integration review. Luna handles the other responsibilities, including independent
critical review. A role name never proves adequate review depth: unresolved risk
must go back to the parent, not be waived because the designated reviewer ran.

**Lean Delivery** concentrates the same responsibilities on lighter models. Use
it for well-defined work where spending on every specialist is less useful. Its
integration reviewer uses Sol `high`; its decision advisor uses Astra `high`.
All other specialists, including backend and frontend workers, use Luna `max`.
This keeps the expensive specialist allocation narrow while retaining a dedicated
cross-delivery integration review. The lead is separate from these child counts.
The lead must reassess tasks that exceed the assigned specialist's capability.
Calling a reviewer to perform implementation is not a valid cost escalation.

Choose by the actual task and available role descriptions. File count alone says
little about complexity: a small authorization change can carry more risk than a
large mechanical update. A role that requires repeated correction can cost more
than a stronger role completing the work once. These are design tradeoffs;
this catalog does not publish an unmeasured price ranking or savings percentage.

## Smaller catalogs and active teams

Advanced exposes 15 roles, Balanced 12, and Lean 8. Their retained roles follow
the same task-based allocation, but removed responsibilities have explicit owners:

| Removed specialization | Advanced | Balanced | Lean |
| --- | --- | --- | --- |
| Light backend/frontend variants | Regular worker | Regular worker | Regular worker |
| Documentation writer | Parent | Parent | Parent |
| Security sweep | Critical reviewer | Critical reviewer | Critical reviewer |
| Separate design direction | Design lead retained | Advisor | Advisor |
| Unknown-cause diagnosis | Debugger retained | Hard-task specialist | Parent |
| Separate test author | Test engineer retained | Owning worker | Owning worker |
| Coupled implementation, database, infrastructure | Dedicated roles retained | Dedicated roles retained | Parent or separately qualified help |
| Separate test runner | Retained | Retained | Parent; workers run their own checks |

Implementation and independent review remain separate even in Lean. An absent
specialist is not permission to lower acceptance or move irreversible work into
an underqualified role. These are public adaptations, not whole-home exports.

Advanced permits four active children, Balanced three, and Lean two
(total-thread caps of five, four, and three including the lead). Start with one
useful child. Advanced leaves room for disjoint implementation and investigation;
Balanced supports two implementation fronts and a bounded check; Lean favors a
short implementation-then-review sequence. Review the combined artifact after
the writers finish; these examples are not mandatory phases or reserved slots.

The names describe intended delivery complexity and resource allocation, not
subscriptions or measured savings. The smaller public caps are deliberate
adaptations, not copies of a personal installation and not benchmark optima.
No local comparative benchmark establishes superiority of these topologies.

## Parent-mediated routing only

A child returns its result or blocker to the parent, optionally recommending a
role. It never contacts, waits for, or dispatches another child. Role references
in descriptions help the parent choose work; they are not a network of agents
that must already be running. The parent performs the work directly, spawns an
available role with a complete brief, or resumes a suitable completed child with
`followup_task`. Review waits for the actual artifact, not a promised delivery.

## Why `fork_turns: "none"`

A fresh child receives a deliberate brief rather than the parent's accumulated
conversation. This keeps irrelevant history and abandoned assumptions out of a
bounded assignment and makes its inputs easier to review. The tradeoff is that
the parent must provide the necessary context explicitly: accepted decisions,
files, interfaces, constraints, output and validation.

`none` does **not** mean no instructions, no tools or a security boundary. The
child still receives its role and applicable runtime/project instructions and
can inherit environment capabilities. Keep task context small and complete;
do not confuse a shorter prompt with permission isolation.

Omitting the argument is not equivalent to `none`. The inspected upstream V2
parser defaults an omitted/empty value to `all`, accepts `none`, `all` or a
positive integer string, and rejects the older `fork_context` field. See the
[V2 spawn implementation](https://github.com/openai/codex/blob/b979d4f1f04538ba5a5fcc434d499c007bfe1b8c/codex-rs/core/src/tools/handlers/multi_agents_v2/spawn.rs).

Upstream history-fork behavior has evolved. That source revision can apply a
named role even with a full-history fork; it would be incorrect to claim that
every Codex version always rejects that combination or always ignores the role.
This catalog deliberately chooses fresh-context delegation regardless, and the
optional hook enforces that narrower policy where interception is proven.

## Why explicit roles and TOML-owned models

`agent_type` selects a role, not a task nickname or a model. Each published role
has one TOML containing its model, reasoning effort and behavioral instructions.
The runtime's live role catalog or installed files are the source for what can
actually be selected. `list_agents` shows thread activity, not all available roles.

Pinning model and effort together makes the specialist choice reviewable and
avoids inheriting an effort that is unsuitable for another model. The arrangements
exclude call-level overrides to keep one source of configuration for each role.
This is our policy, not a claim that the runtime cannot support overrides. The
[official subagent documentation](https://developers.openai.com/codex/multi-agent)
explains configuration inheritance and custom-agent precedence. The inspected
upstream spawn code resolves requested overrides before applying the role.

Read-only and implementing roles have different jobs. A review should return
findings and evidence, while an implementation assignment should return a diff
and validation. The lead retains integration and acceptance responsibility.

## Why task names and follow-ups matter

Use a short task name for the bounded assignment and put the full objective in
the brief. The task name identifies the spawned work; `agent_type` identifies the
specialist configuration. They are different fields.

A client may show the hierarchical task path (for example,
`/root/review_api_contract`) in its activity label instead of the optional
nickname. Prefer descriptive task names such as `review_api_contract` or
`validate_installation`, following the exposed schema's character rules.
Nickname customization is neither required for delegation nor a promise about
how a particular client renders the task.

In the inspected V2 source, the spawn response includes `task_name` and
`nickname`, but the subsequent
[activity item](https://github.com/openai/codex/blob/b979d4f1f04538ba5a5fcc434d499c007bfe1b8c/codex-rs/protocol/src/items.rs#L352-L358)
contains the thread ID, task path and activity kind without a nickname. The
[public TUI activity renderer](https://github.com/openai/codex/blob/b979d4f1f04538ba5a5fcc434d499c007bfe1b8c/codex-rs/tui/src/multi_agents.rs#L286-L340)
uses that path. Thus a valid nickname can coexist with a path-only activity
label. The closed ChatGPT/Work renderer was not inspected; its exact label
behavior remains unverified. Changing a role's nickname pool does not change
this event contract.

`send_message` queues information for an existing child. `followup_task` requests
another turn, including for a finished child, retaining that child's history.
Use a follow-up for a correction that benefits from the child's prior context;
spawn a fresh child for a new independent assignment. The upstream handlers make
the distinction explicit: [queue-only message](https://github.com/openai/codex/blob/b979d4f1f04538ba5a5fcc434d499c007bfe1b8c/codex-rs/core/src/tools/handlers/multi_agents_v2/send_message.rs)
and [turn-triggering follow-up](https://github.com/openai/codex/blob/b979d4f1f04538ba5a5fcc434d499c007bfe1b8c/codex-rs/core/src/tools/handlers/multi_agents_v2/followup_task.rs).

Use the native tool namespace and schema exposed by your runtime. A configured
namespace does not mean those tools are callable inside every code execution tool.
Do not substitute an external agent process or a shared file for native delegation.

## Why bounded concurrency and one delegation level

Parallelism helps when children can make independent progress. It also increases
token use and contention for shared files, test services and the lead's review
capacity. Reserve capacity, keep writing scopes disjoint, and serialize interacting
changes. When the cap is reached, advance independent local work; wait only when
the next useful step depends on a child.

The supplied caps are configuration values, not a promise to launch that many
children at once. Counting differs across versions; see [validation](validation.md).
A completed child appearing in a thread list does not by itself establish that it
still occupies an active slot. Do not invent a close tool that your runtime lacks.

Only the lead delegates so it can see the full work allocation, cost exposure
and integration risks. This restriction lives in the snippets and role instructions.
The spawn-contract hook checks arguments; it does not establish caller ancestry
or mechanically guarantee a recursion limit.

## Adaptive waiting

The lead should work while useful independent work remains. When only delegated
work remains, choose a native event-aware wait using expected duration,
complexity, workload and meaningful progress signals, not file count alone.
Keep this decision in the existing optional `codex-orchestration` skill; the
insertable rules contain only a concise fallback. No new hook is required.

```text
Useful independent work? -- yes --> advance it
           |
           no
           v
Native wait --> message/result --> act on the new evidence
           |
           timeout --> investigation due? -- yes --> inspect a concrete signal
                                |
                                no --> wait again
```

Use the configured five-minute default for ordinary delegated work. A brief
check expected to finish quickly can warrant an explicit one-minute window;
a lengthy build or coupled implementation can warrant a longer supported window.
These are starting points, not fixed task classes. Set a separate, task-appropriate
point to investigate missing progress. A running status or an expired wait is
not proof of progress, failure or a stall. Do not extend waits indefinitely when
expected milestones are missing, or interrupt healthy work after every timeout.

| Scenario | What changes |
| --- | --- |
| Child completes in 20 seconds | Its queued completion can end the five-minute wait early. |
| Child works silently for eight minutes | The longer default can reduce empty returns to the parent model; it does not shorten the child's work. |
| Parent explicitly requests 30 seconds | The one-minute floor applies; the five-minute default does not. |
| Parent already requests five minutes | No change to that wait. |
| Child emits frequent non-actionable messages | Messages still wake the parent; report blockers, meaningful milestones and final artifacts instead. |
| Child stalls | A longer window can postpone detection; the independent investigation point limits this tradeoff. |
| Parent polls a terminal or code-mode cell | Those tools have separate limits and arguments; these V2 settings do not change them. |

### Context, tokens and the harness

The native [wait handler](https://github.com/openai/codex/blob/dfaf451426868c22e6859f5494150fd6338c3257/codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs)
waits on queue activity or a deadline without sampling the model inside that
wait. Repeated short waits can nevertheless cause repeated parent model calls
after the tool returns. Each sampling step builds input from the parent's own
[conversation history](https://github.com/openai/codex/blob/dfaf451426868c22e6859f5494150fd6338c3257/codex-rs/core/src/session/turn.rs).
That is not equivalent to resending all bytes every time: the
[client](https://github.com/openai/codex/blob/dfaf451426868c22e6859f5494150fd6338c3257/codex-rs/core/src/client.rs)
also supports incremental WebSocket requests. Logical context, transmitted bytes,
cached input and account quota accounting must not be conflated.

The parent receives explicit child communications and final-result/error notices,
not the child's complete transcript. [Agent listing and completion monitoring](https://github.com/openai/codex/blob/dfaf451426868c22e6859f5494150fd6338c3257/codex-rs/core/src/agent/control.rs)
read status and deliver notifications; listing does not inspect the child's
reasoning or prove progress. `fork_turns: "none"` controls initial parent-to-child
history inheritance, not what results come back. A child still consumes its own
model tokens while the parent waits. Do not assume that ending the parent's turn
guarantees a later completion notice will automatically start another turn.

Active [goals can automatically continue an idle thread](https://github.com/openai/codex/blob/dfaf451426868c22e6859f5494150fd6338c3257/codex-rs/ext/goal/src/runtime.rs).
The [empty-turn guard](https://github.com/openai/codex/blob/dfaf451426868c22e6859f5494150fd6338c3257/codex-rs/ext/goal/src/accounting.rs)
counts text and tool calls as activity, so it does not identify every unproductive
polling loop. Longer native waits and better instructions mitigate avoidable
returns; they do not change that harness behavior. We have not established a
specific local harness bug or measured a reduction in five-hour quota usage.
Preventing every redundant automatic turn would require a separate upstream
change and regression evidence, not a stronger claim about these settings.

The source review above is pinned to 2026-09-13. See [configuration](configuration.md#native-child-wait-settings)
for exact values and rollback, and [validation](validation.md) for what was run.

## Evidence and references

### Prompt and skill design

The instruction review uses OpenAI's September 11, 2026 guidance,
[Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra).
Skill discovery stays narrow; AGENTS excerpts invoke optional procedures only
for relevant situations. Role prompts identify the artifact, responsibility and
safe operating boundary without prescribing a universal sequence of reads or tests.
Delegation rules retain the exact fields needed by the measured runtime.

Local checks using disposable fixtures can proceed within the assigned scope;
publication, production access and unrelated changes require the applicable
authorization. Implementation briefs ask for a completed, verified change rather
than a first draft. The same instructions serve several model families, so
leaner text is a design choice to evaluate, not proof of equal behavior across
models. Real-run evidence remains necessary after prompt changes.

The source links above pin the revision inspected while building this catalog;
they are not proof that an installed binary has the same implementation. Runtime
acceptance must report its own version and observed tool events. In addition to
the linked source, consult:

- [Official configuration reference](https://developers.openai.com/codex/config-reference)
- [Official AGENTS.md guide](https://developers.openai.com/codex/guides/agents-md)
- [Official skills documentation](https://developers.openai.com/codex/skills)
- [Official hooks documentation](https://learn.chatgpt.com/docs/hooks)

Review changes in the runtime before updating a manifest's compatibility claim.
Keep operational measurements in validation records, not in the installed
instruction snippet as an undated universal guarantee.
