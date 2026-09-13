# Configuration

## Configuration items

| Item | Authoritative location | Purpose and rollback |
| --- | --- | --- |
| Lead model and effort | Each arrangement's `config.toml` | Select the root agent; restore the prior fields in your installation to undo a change. |
| V2 and namespace | Each arrangement's `config.toml` | Enable the required orchestration tools; revert only installed fields, preserving other feature settings. |
| Concurrency cap | Each arrangement's `[features.multi_agent_v2]` table | Bound total active threads, including the lead in the target V2 runtime; consult counting evidence before adjusting. |
| Specialist model, effort and behavior | Each `agents/<name>.toml` | Define one role; restore its reviewed prior revision, not a whole personal config. |
| Optional hook command and matcher | `hooks/spawn-contract/hooks.example.json`, adapted at installation | Review and trust the local command; remove only this handler to uninstall. |
| Optional skills | `skills/<skill-name>/SKILL.md`, declared in each manifest | Delegation and engineering decision procedures; inline triggers in the with-skill snippet include a fallback when absent. |

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
| 0.1.0 | Introduce two lead/specialist combinations, V2 fragments and optional spawn contract | Share independently installable delegation arrangements | Remove the selected roles, instruction section and optional components; restore only the original configuration fields. |
