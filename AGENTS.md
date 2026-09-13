# Maintaining this catalog

Tracker: github — rafaelob/fleet-codex. Issues hold intent, acceptance and delivery evidence.

This file guides work on the catalog itself. Installation snippets are the
`AGENTS*.snippet.md` files under `arrangements/`; do not install this file as an
orchestration policy.

- `arrangements/` owns lead/subagent TOMLs and insertable instruction sections.
- `skills/`, `plugins/` and `hooks/` contain independent, optional components.
- `docs/` explains installation, tradeoffs and sanitized runtime evidence.
- Run `python -X utf8 scripts/validate_catalog.py`,
  `python -X utf8 scripts/validate_components.py` and
  `python -X utf8 -m unittest discover -s tests -v` from this repository root.
  These use Python 3.11+ and its standard library; no package manager is required.
- Keep installable content, code, Issues and PRs in English; translated guides
  may supplement English documentation. Preserve component licenses and notices.
- Never include personal configuration, credentials or raw runtime sessions.
  Keep experimental runtime fixtures in the ignored `.runtime-validation/` area
  and remove owned temporary credentials and processes when testing ends.
- Follow `CONTRIBUTING.md` for package contracts and evidence. Update
  `docs/CHANGELOG.md` for a delivered change; static checks do not prove model,
  plugin or hook integration.
