# Contributing

An arrangement describes a useful way to divide work between one lead and its
subagents. Explain the kinds of work it serves, the tradeoffs, and when a user
should choose another arrangement. Do not claim cost savings or quality gains
without identifying the measurements behind them.

All source code, configuration, agent instructions, skills, issues and pull
requests use English. Optional documentation translations may use another
language; keep the English guide authoritative and link translations from it.

## Ways to contribute

- Share a new combination through the New arrangement issue form or a PR.
- Correct instructions, configuration, compatibility evidence or bugs in an
  existing arrangement through the Correction issue form or a focused PR.
- Share or improve a standalone skill, plugin, hook, tests or installation guide, with evidence
  proportional to the behavior changed.

An issue is useful for discussing a substantial change, but not required before
a small correction. Search existing issues and PRs before opening another.

## Send a pull request

1. Fork this repository on GitHub and clone your fork.
2. Create a descriptive branch, such as `add-my-arrangement` or
   `fix-lean-delivery-installation`.
3. Make one coherent change. For corrections, show the current problem and the
   resulting behavior; for a new arrangement, include the complete package below.
4. Run the checks and relevant runtime validation. Review your complete diff for
   private configuration, credentials and unrelated files.
5. Commit and push the branch to your fork, then open a PR targeting this
   repository's `main` branch. Fill in the provided PR template in English.
6. Address review feedback in the same PR. Maintainers review compatibility,
   licensing and evidence before merging.

You do not need collaborator access to submit a PR from a public fork. The
repository provides issue forms, a PR template and CI checks; no private
coordination tooling or installation is required to contribute.

## Package contract

Create `arrangements/<unique-id>/` with:

| File | Purpose |
| --- | --- |
| `arrangement.toml` | Package identity, version, author, license, target Codex version and relative component paths; report tested support separately |
| `config.toml` | Lead model/effort, V2 settings and thread cap only |
| `agents/*.toml` | One complete configuration per specialist |
| `AGENTS.snippet.md` | Standalone orchestration instructions for user or project scope |
| `README.md` | Use cases, model/role mapping, installation link, limitations and evidence |

An optional with-skill snippet must invoke the packaged skills by their exact names
and describe when to use them. Declare optional_skills as a nonempty list of
relative directories; each must resolve inside this repository and contain SKILL.md.
The with-skill snippet is valid only with that nonempty list; omit both when no
skill variant is provided. Components have no download-on-use dependencies or
personal paths.
The required thread cap is features.multi_agent_v2.max_concurrent_threads_per_session;
the optional root agents table may contain only default subagent model and
reasoning-effort values.
The V2 table also accepts optional `min_wait_timeout_ms`, `default_wait_timeout_ms`
and `max_wait_timeout_ms`. Values must be integers from 0 through 3600000; after
applying native defaults, minimum <= default <= maximum must hold. See
[configuration](docs/configuration.md#native-child-wait-settings). Explain any
different choice without claiming unmeasured token savings.
An optional hook is a contained relative directory with a README.md documenting
installation, supported runtime and entrypoint; its implementation may use any
supported language and does not require a guard.py file.

Use the current manifests as examples of schema version 1. The validator is the
executable contract. The five core role keys are `name`, `description`, `model`,
`model_reasoning_effort` and `developer_instructions`; optional `nickname_candidates`
is English display metadata only. When present it is a nonempty list of strings:
each candidate is trimmed, nonblank, unique after trimming, and limited to ASCII
letters, digits, spaces, hyphens and underscores. Filename and role name must
match. Put the role's behavior in its instructions, without requiring another
skill, plugin, MCP server, personal configuration or private service.

Keep credentials, provider connections, permissions, hooks and skills out of role
TOMLs. If a workflow needs an optional public capability, document it separately
with installation, license, required access and what happens when it is absent.
Do not include any credential, local session, transcript, database, login cache,
private project identifier or personal absolute path.

## Verify before opening a PR

For independent components, use `skills/<skill-name>/`, `plugins/<plugin-name>/`
or `hooks/<hook-name>/`, not an arrangement's version directory. A component may
serve any arrangement and must have its own purpose, license/provenance,
installation/removal instructions and evidence. A plugin may bundle skills,
public MCP configuration and hooks; follow the [plugin contribution contract](plugins/README.md).
Do not add a mandatory MCP connection or skill dependency to an agent role.
The [skill guide](skills/README.md) explains invocation and optional instruction
sections. A focused component PR need not add or modify an arrangement.

Run with Python 3.11 or newer; no package installation is necessary:

```text
python -X utf8 scripts/validate_catalog.py
python -X utf8 scripts/validate_components.py
python -X utf8 -m unittest discover -s tests -v
```

Also install the arrangement into a clean user or project scope and demonstrate
one real delegation: selected role, resolved model/effort, returned artifact and
parent verification. State the exact CLI version, platform, date, failures and
unmeasured claims. Do not publish authentication material or raw transcripts.
An unavailable required check remains a blocker, not a pass.

For a component-only change, exercise that component's real entry point instead
of unrelated model configurations. Plugin structural preflight is not full
upstream-schema validation or installation proof: validate the selected manifest
dialect and demonstrate the bundled capabilities in the named runtime. Report
zero contributed plugins as zero, not as a passing plugin integration test.

For hooks, show that an allowed call proceeds and a denied call cannot execute
through the supported runtime path. A script test alone is insufficient. Explain
which tools/events are covered and which guarantees remain instructions only.

CI validates packages and executable behavior without model credentials. External
contributors' code runs with read-only repository permissions and no secrets.

## Review and updates

Use a PR for new arrangements and changes to published ones. Bump the arrangement
version when its behavior changes, update its evidence, and add a changelog entry.
Preserve contributor attribution and licenses, including notices on derived
skills. A copied instruction is still a licensed work.

Keep executable tests focused on behavior: malformed configuration, broken paths,
escaping references, and hook decisions. Documentation consistency belongs in
the package validator and review, not snapshot tests of prose.
