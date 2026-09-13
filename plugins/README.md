# Optional workflow plugins

This directory accepts self-contained plugin contributions that improve an agent
workflow. A plugin may package skills, public MCP connections, lifecycle hooks,
or a useful combination. Plugins are separate from arrangements and optional;
the initial release has no installable plugin bundle or marketplace entry.
Standalone skills already live in [skills/](../skills/README.md).

## Choose the supported package format

The [official packaging guide](https://developers.openai.com/plugins/build/plugins),
checked on 2026-09-12, recommends the portable Agent Plugins format for new
packages. It also documents the supported Codex compatibility format generated
by the built-in plugin creator. State your format and tested runtime explicitly:
support in current documentation is not proof for every older Codex release.

```text
plugins/<plugin-name>/
  plugin.json                 portable manifest
  skills/<skill-name>/         optional bundled skills
  mcp.json                    optional portable MCP configuration
  hooks/hooks.json            optional lifecycle hooks
  scripts/                    optional executable implementation
  assets/                     optional package assets
  README.md                   installation, access, evidence and removal
  LICENSE                     license; include notices for derived components
```

For a portable package, declare the Agent Plugins schema in root `plugin.json`.
OpenAI-specific presentation, registered connection mappings and hook settings
belong in `extensions.com.openai`. Portable skills and MCP use the fixed root
locations `skills/` and `mcp.json`.

The Codex compatibility layout instead uses `.codex-plugin/plugin.json` and can
use `.mcp.json`. Its manifest directory contains only the manifest, not the
skills or hook scripts. Do not rename `.mcp.json` to `mcp.json` as a migration:
the portable MCP format also requires each server's transport `type`. If both
manifest formats exist, document precedence; the OpenAI inline extension replaces
the compatibility overlay, rather than merging both configurations.

## Contribution contract

1. Add a uniquely named folder whose name matches the manifest's plugin name.
   Include meaningful version, description, author and license metadata.
2. Package only capabilities the workflow needs. Keep referenced files inside
   the plugin; no personal absolute paths, escaping symlinks or references into
   a contributor's installed Codex home.
3. Document each MCP server's purpose, transport, permissions, external data flow,
   authentication setup and possible cost. Never include tokens, cookies, login
   caches, private endpoints or automatic credential copying. Local server
   dependencies need explicit, reproducible installation and version evidence.
4. Document hook events, matchers, commands and failure behavior. Installation
   does not establish trust: users must review and trust the exact definition.
   Use the runtime's plugin-root mechanism for script paths; do not copy trusted
   hashes or claim hooks provide a security sandbox.
5. Include license/provenance for bundled skills and scripts. When packaging a
   shared catalog skill, name its canonical source and reproducible packaging
   step; the installed bundle must not depend on a sibling directory.
6. Supply installation, update, disable/removal and rollback instructions, plus
   exact runtime/platform/date and sanitized evidence for the capabilities
   actually shipped. MCP evidence must reach a real authorized server; hooks
   need real interception and negative-path evidence, not only script tests.

Run `python -X utf8 scripts/validate_components.py` from the repository root for
structural preflight, then the current upstream schema/authoring validator for
your chosen format and real installation tests. Preflight does not execute plugin
commands or establish complete schema, security, authentication or runtime support.
Follow [Contributing](../CONTRIBUTING.md) to submit a focused PR.

## Distribution and installation

A reviewed plugin can be distributed through a repo/team marketplace following
the official guide. Declare each entry as available for optional installation;
do not install it by default or modify a user's personal marketplace on their
behalf. An empty directory is not an installable marketplace: this repository
does not advertise a marketplace installation command before a real plugin and
validated entry exist.

Publishing here is separate from submission to OpenAI's universal directory.
See [official plugin submission](https://developers.openai.com/plugins/deploy/submission)
for that additional review process. Never imply that a community contribution is
endorsed or approved by OpenAI.
