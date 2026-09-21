# Configuration

## Configuration items

| Item | Authoritative location | Purpose and rollback |
| --- | --- | --- |
| Lead model and effort | Each arrangement's `config.toml` | Select the root agent; restore the prior fields in your installation to undo a change. |
| V2 and namespace | Each arrangement's `config.toml` | Enable the required orchestration tools; revert only installed fields, preserving other feature settings. |
| Concurrency cap | Each arrangement's `[features.multi_agent_v2]` table | Bound total active threads, including the lead in the target V2 runtime; consult counting evidence before adjusting. |
| Native child waits | Each arrangement's `[features.multi_agent_v2]` table | Reduce empty wait returns; restore only your previous wait fields to roll back. |
| Specialist model, effort and behavior | Each `agents/<name>.toml` | Define one role; restore its reviewed prior revision, not a whole personal config. |
| Optional hook command and matcher | `hooks/spawn-contract/hooks.example.json`, adapted at installation | Review and trust the local command; remove only this handler to uninstall. |
| Optional skills | `skills/<skill-name>/SKILL.md`, declared in each manifest | Delegation and engineering decision procedures; inline triggers in the with-skill snippet include a fallback when absent. |

## Native child wait settings

All three arrangements use the same wait settings in version 0.4.0:

| Field under `features.multi_agent_v2` | Native baseline | Catalog value | Meaning |
| --- | --- | --- | --- |
| `min_wait_timeout_ms` | 10000 (10 seconds) | 60000 (1 minute) | Floor for an explicitly requested child wait; shorter requests are raised to this value. |
| `default_wait_timeout_ms` | 30000 (30 seconds) | 300000 (5 minutes) | Used only when the child wait omits its timeout. |
| `max_wait_timeout_ms` | 3600000 (1 hour) | Not overridden | Largest permitted request; a larger request is rejected, not clamped. |

These are event-aware waits, not mandatory delays: queued child messages and user
input can end a wait early. A requested 30-second wait becomes one minute, not
five minutes. They do not change terminal polling, code-mode waits, goal budgets,
goal continuation, child execution time or the account's usage limits.

The validator permits optional integer wait fields from 0 through 3600000,
including zero, matching the inspected runtime. Effective values, including
omitted native defaults, must satisfy minimum <= default <= maximum. Setting
only a 60000 minimum is invalid against the native 30000 default; merge both
published fields. An existing maximum below 300000 needs deliberate reconciliation.

Defaults and behavior were inspected on 2026-09-13 in the pinned upstream
[configuration implementation](https://github.com/openai/codex/blob/dfaf451426868c22e6859f5494150fd6338c3257/codex-rs/core/src/config/mod.rs)
and [V2 wait handler](https://github.com/openai/codex/blob/dfaf451426868c22e6859f5494150fd6338c3257/codex-rs/core/src/tools/handlers/multi_agents_v2/wait.rs).
Check the installed runtime after upgrades. See [adaptive waiting](orchestration.md#adaptive-waiting)
for task-based choices and limitations; these values are not a measured optimum.

## Baseline

There are no runtime package dependencies. Python 3.11+ runs the validator,
tests and optional hook. The target Codex baseline is declared in each
arrangement's manifest; evidence and limitations live in [validation.md](validation.md).
The arrangements contain no permission, credential, plugin or MCP configuration.
Separately contributed [plugins](../plugins/README.md) may declare public optional
capabilities; installing an arrangement never installs those capabilities.

Role files include six English `nickname_candidates` per role. These playful
public-figure references are display metadata, not affiliations, personas or
role/model selection. Contributors may omit the field to use Codex defaults.
The validator requires a nonempty list of trimmed, nonblank, unique strings
containing only ASCII letters, digits, spaces, hyphens and underscores. This
prevents the invalid-character failure that can make the loader ignore an entire
role file. The client may still display the task path instead of the nickname;
changing this metadata does not control every client's labels. See
the [role parser](https://github.com/openai/codex/blob/b979d4f1f04538ba5a5fcc434d499c007bfe1b8c/codex-rs/agent-roles/src/agent_role_config.rs)
and [default nickname selection](https://github.com/openai/codex/blob/b979d4f1f04538ba5a5fcc434d499c007bfe1b8c/codex-rs/core/src/agent/control/spawn.rs).

## Change log

| Version | Change | Reason | Rollback |
| --- | --- | --- | --- |
| 0.4.0 (2026-09-20) | Lower Advanced Delivery's total-thread cap from five to four (three active children, equal to Balanced); rewrite the orchestration skill and every AGENTS snippet around bounded, single-mission delegation | Treat the configured cap as a ceiling, not a target, and stop the context cost of reusing or repeatedly waking a child after its mission is accepted | Restore `max_concurrent_threads_per_session = 5` in Advanced Delivery's `config.toml`; restore the prior skill and snippet wording. No other arrangement's config changed. |
| 0.3.0 (2026-09-13) | Set one-minute minimum and five-minute default child waits; add adaptive waiting guidance | Reduce empty parent wait returns without changing budgets or the execution topology | Restore only prior wait fields and the affected instruction/skill sections; remove these fields only if they were previously absent. |
| 0.2.0 (2026-09-13) | Add Balanced Delivery; rebalance models, reduce catalogs to 15/12/8 roles and total-thread caps to 5/4/3; require parent-mediated routing | Match reasoning to responsibility and reduce selection and coordination overhead | Reinstall reviewed prior role cards and matching snippets/config fields together. Follow the upgrade removal list; preserve credentials and unrelated settings. |
| 0.1.0 | Introduce two lead/specialist combinations, V2 fragments and optional spawn contract | Share independently installable delegation arrangements | Remove the selected roles, instruction section and optional components; restore only the original configuration fields. |
