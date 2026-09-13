# Validation and compatibility

Validation distinguishes a parsed package, an executable hook and a functioning
integration. None substitutes for the others.

The sanitized [runtime evidence record](runtime-evidence.json) identifies the
measured scenarios and their outcomes. A completed model turn, a copied role file
or a configured cap alone is not a completed implementation or saturation test.

## Current measured status

Version 0.1.0 is a community catalog preview, not a certification of every role,
platform or concurrency limit. Known integration limits are listed below.

The initial 2026-09-12 Windows run verified native hook interception on allowed and
blocked paths, three completed role selections, and user/project configuration
loading. Its first native file-edit attempt left the fixture unchanged and its
behavioral check red. After temporary-directory isolation, a fresh native
backend-worker changed the source, preserved the test file, and passed that test
when independently executed by the external parent. The native parent and a
separate reviewer then encountered `CreateProcessAsUserW failed: -1073283067`;
the reviewer could not read or test the artifact. A no-model comparison isolated
that failure to Store-packaged PowerShell in the tested sandbox, independently
of the test's process containment. The Store installation was not changed.
Concurrency saturation and slot release were not run. Full runtime acceptance
on this environment remains blocked; this is not evidence of a role-card defect.

A no-model follow-up reproduced the stall with a standalone Windows sandbox
`echo` command, without authentication, app-server or code mode. This narrows
the failing path. Changing only the test process's `TEMP` and `TMP` to an owned
empty directory then made that same command pass, with a native `START` to
`SUCCESS` interval of 66 ms. No sandbox or private-desktop control was disabled.
See [Windows test isolation](windows-sandbox.md). This correction enabled the
measured child file edit, but does not explain or resolve the later process-startup error.

Two completed roles returned a token supplied in their prompts. Those responses
are not evidence that a file was read. The evidence record keeps response,
configuration and artifact verification separate.

## Target baseline

The initial arrangements target `codex-cli 0.155.0-alpha.3.10` with Multi-Agent V2.
Model names and reasoning efforts are explicit in each TOML; availability depends
on the installing account and runtime. An unavailable model is an error to resolve,
not permission to substitute a different model silently.

The fragments set `features.multi_agent_v2.max_concurrent_threads_per_session`
to 6 and 7. The target binary's prompt-input output confirms those are total
slots including the lead: at most 5 and 6 concurrent children, respectively.
The legacy `agents.max_concurrent_threads_per_session` is a child cap; this
binary adds one when translating it into a V2 total. Mixing the two settings
would misstate capacity. The [pinned configuration resolver](https://github.com/openai/codex/blob/b979d4f1f04538ba5a5fcc434d499c007bfe1b8c/codex-rs/core/src/config/mod.rs#L2500)
explains that translation. Prompt-input inspection proves configuration resolution,
not running-child saturation or slot release; those require separate live probes.

## Executable checks

```text
python -X utf8 scripts/validate_catalog.py
python -X utf8 scripts/validate_components.py
python -X utf8 -m unittest discover -s tests -v
```

The validator checks real package references, configuration parsing and selected
private-dependency patterns in manifest-referenced configuration, instructions,
role cards, skill instructions and hook documentation. This is not a comprehensive
secret scanner: review the entire proposed diff, including READMEs, examples,
licenses and supplemental files, before publishing. Unit tests exercise malformed and escaping configurations
and the hook process's allow/deny contract. CI runs these without account
credentials; it does not start paid model sessions.

Component preflight checks standalone skill files and optional plugin package
structure. It does not parse YAML frontmatter or replace upstream schema and
real installation checks. The first release has two standalone skills and zero
plugin bundles; zero plugins is not a passing plugin integration test. Directory
escape tests use real symlinks where available and a Windows junction otherwise.

## Runtime acceptance

For a fully runtime-validated release, evidence must identify the exact CLI, date and platform
and show:

1. User and project installation load the declared roles and effective settings.
2. A read-only explorer, authorized implementer and independent reviewer return
   artifacts that the parent verifies.
3. The optional hook intercepts a permitted spawn and rejects a disallowed spawn
   through the real V2 tool path.
4. Concurrency measurements distinguish running children from completed threads
   and state whether the root occupies a slot.

Record the actual tool events and resolved configuration. Model self-reports,
silent hooks or an empty test selection do not establish these claims. Publish
only a sanitized report; keep authentication and raw sessions out of the catalog.
