## Arrangement or component and purpose

Describe the intended work, division of responsibility and tradeoffs.

## Changes

List configuration, instruction, skill, plugin or hook changes and licensing provenance.

## Functional evidence

Provide exact Codex version, platform and sanitized results for installation,
role/model selection and delegation. For hook changes, include real allow/deny
evidence. State unavailable or unmeasured checks explicitly.
For component-only PRs, demonstrate the changed component's real entry point.
For plugins, identify the manifest format, bundled capabilities and upstream
schema check; structural preflight is not installation evidence.

## Checks

- [ ] Catalog validator and relevant executable tests pass.
- [ ] No credentials, personal paths, private services or whole-home config dumps.
- [ ] Component licenses and notices are preserved.
- [ ] Version, installation instructions and changelog describe the final change.
