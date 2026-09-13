# Install an arrangement

Use an existing authenticated Codex CLI installation. Check `codex --version` and
the [validation record](validation.md); these packages target Multi-Agent V2 and
do not silently fall back to V1. You need access to the named models. Python 3.11+
is needed only for the optional hook and local validation.

## Upgrading from 0.1.0

Copying a smaller roster over the old directory does not remove obsolete cards.
Back up only the arrangement files you installed and identify which cards are
yours; never clear the entire agents directory or Codex home.

- Advanced removes `backend-worker-light.toml`, `frontend-worker-light.toml`,
  `docs-writer.toml`, and `security-sweep.toml`.
- Lean removes those four plus `design-lead.toml`, `debugger.toml`,
  `test-engineer.toml`, `hard-task-specialist.toml`, `database-engineer.toml`,
  `infra-sre.toml`, and `test-runner.toml`.
- Balanced is new. When switching arrangements, compare its listed cards to your
  installed set and remove only confirmed obsolete arrangement cards.

Move removed cards outside every loaded agents directory, preserving your own
custom roles. Install the selected roster and its matching instruction and
configuration fragments. A card left in a loaded directory remains available.
For rollback, restore prior arrangement cards and matching fragments together;
never restore a whole home over newer credentials or unrelated configuration.

## Choose a scope

| Component | User scope | Project scope |
| --- | --- | --- |
| Configuration | `$CODEX_HOME/config.toml` (normally `~/.codex/config.toml`) | `<project>/.codex/config.toml` |
| Agent TOMLs | `$CODEX_HOME/agents/` | `<project>/.codex/agents/` |
| Instructions | `$CODEX_HOME/AGENTS.md` | `<project>/AGENTS.md` |
| Optional skill directories | `~/.agents/skills/<skill-name>/` | `<project>/.agents/skills/<skill-name>/` |
| Optional hooks | `$CODEX_HOME/hooks.json` | `<project>/.codex/hooks.json` |

`CODEX_HOME` selects a Codex home; the arrangement names do not require separate
homes or a special installation mode. Skill discovery uses `.agents/skills` as described in
the [official skill documentation](https://developers.openai.com/codex/skills).
Project configuration and hooks require a trusted project. Inspect existing user
and project configuration before choosing the scope: more specific settings may
override your selection, and same-named agents can shadow other definitions.

## Install the core package

1. Clone or download a reviewed revision of this repository. Choose exactly one
   arrangement. Record the revision and save a local backup of each destination
   you will edit. Do not commit backups containing personal configuration.
2. Open the arrangement's `config.toml`. Merge its lead settings and the fields
   under `[features]` and `[features.multi_agent_v2]` into the chosen
   destination. TOML tables must not be declared twice. Preserve unrelated fields.
   Keep the cap under the V2 table: the older `[agents]` cap is interpreted
   differently by this runtime. Do not copy that legacy cap into this fragment.
3. Copy the chosen arrangement's `agents/*.toml` into the destination `agents/`
   directory. Review every name collision before replacing a file. Do not combine
   different arrangements' same-named roles in one scope.
4. Insert the content of `AGENTS.snippet.md` into the appropriate AGENTS.md, without
   replacing its other instructions. If an AGENTS.override.md is active at that
   scope, reconcile with it: a lower-priority file may not be loaded.
5. Start a new Codex session in the target project. Inspect warnings, available
   roles and effective settings. Existing sessions may retain earlier settings.

Model and effort are pinned in the role TOMLs. Do not override them at spawn time.
The snippets deliberately require `agent_type` and `fork_turns: "none"`; supply
the child's necessary context in the task brief and use the current native tool
schema for the task name and message. Only the lead delegates.
Read [the orchestration rationale](orchestration.md) for the reasons behind
fresh context, role selection, model ownership, concurrency and follow-ups.

The files do not configure MCP servers, plugins, credentials, approval policies or
sandbox permissions. Subagents can inherit tools and permissions from your existing
environment. A role described as read-only is a behavioral instruction, not an
independent security sandbox.

## Optional skills

Copy the chosen directories from `skills/`, including each LICENSE and NOTICE,
to the chosen skill location. The manifests list both optional skills:

- `codex-orchestration`: invoke `$codex-orchestration` before bounded delegation
  or reconciliation of worker deliveries.
- `pragmatic-programmer`: invoke `$pragmatic-programmer` when choosing a boundary
  or reversible first step, diagnosing unexplained success, checking duplicated
  knowledge, or handling shared state and finite resources.

Use `AGENTS.with-skill.snippet.md` instead of the standalone orchestration snippet;
do not install both. Its inline rules name the skill at the relevant situation.
Verify each installed skill is discoverable before relying on its invocation.
Use the runtime's Skill tool with the exact name when exposed; otherwise follow
its native loading mechanism. Codex's `$skill-name` prompt syntax is not a
guarantee that a tool literally named `Skill` exists. The
[skill guide](../skills/README.md) explains this distinction.
If a skill is absent, follow the snippet's fallback without inventing a tool or
requiring a private installation. You may install either skill independently.
If Pragmatic Programmer is not selected, omit its optional engineering section.

## Optional plugins

Plugins are independent components in [plugins/](../plugins/README.md), not part
of either arrangement's configuration. A contributed plugin may bundle skills,
MCP connections and hooks, with its own installation and access requirements.
The initial release does not include an installable plugin bundle. Review each
future plugin's manifest, dependencies and runtime evidence before installing;
installation does not authorize external data sharing or automatically trust hooks.

## Optional spawn hook

Follow [the hook guide](../hooks/spawn-contract/README.md). Copy the script to a
stable local path, replace the example command with your actual Python and script
paths, and merge its matcher into the chosen hooks.json. Quote paths containing
spaces for your platform. Enable hooks only if you choose to install them.

Review and trust the exact hook in Codex's `/hooks` interface. Do not copy someone
else's trust hashes. Hook sources are additive: project hooks do not replace user
hooks, and multiple matching handlers can all run. Do not install the same hook
at both scopes. Verify real interception using the guide before relying on it.

## Check the installation

Run the catalog checks from the downloaded repository:

```text
python -X utf8 scripts/validate_catalog.py
python -X utf8 scripts/validate_components.py
python -X utf8 -m unittest discover -s tests -v
```

In a disposable project, ask the lead:

```text
Delegate a read-only map of this project's entry point to explorer, with an
explicit role and no history fork. Have it cite the decisive file. Verify its
answer yourself and report the child's resolved model and effort from the actual
runtime record, not its self-description. Do not change files.
```

Then use a small authorized edit and an independent review to exercise an
implementer and reviewer. Compare actual loaded roles with the arrangement, and
check for unexpectedly inherited tools. Treat missing roles, unavailable models,
hook warnings or failed checks as installation failures.

On Windows, isolated test runners should also isolate their temporary directory
before launching Codex. See [sandbox startup diagnostics](windows-sandbox.md)
for the measured failure and the fix that preserves sandbox controls.

## Update or remove

Review the diff between revisions before updating. Compare your current files
with the saved installation revision so your later edits are preserved. Remove
only the installed roles, the inserted instruction section and the selected hook
entry; remove the skill directory only if nothing else uses it. Restore only the
configuration fields you changed from the recorded prior values. Restart Codex
and confirm the old arrangement no longer appears. No automatic installer or
uninstaller modifies your environment.
