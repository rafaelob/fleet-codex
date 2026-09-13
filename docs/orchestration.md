# Why these orchestration choices

These arrangements package a delegation policy, not a replacement for your
AGENTS.md or personal Codex configuration. Insert only the suggested section and
merge only the supplied TOML fields. Keep the longer explanations in this guide
instead of loading them into every conversation.

## Choose by complexity and cost intent

**Advanced Delivery** assigns more capable specialist models to difficult design,
advice, coupled implementation and critical review. Use it when uncertainty and
business impact justify more reasoning across several responsibilities.

**Lean Delivery** concentrates the same responsibilities on lighter models. Use
it for well-defined work where spending on every specialist is less useful. Its
integration reviewer uses Sol `high`; its critical reviewer uses Astra `high`.
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
