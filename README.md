# fleet-codex

Share complete, opinionated combinations of a Codex lead agent and specialist
subagents. Choose an arrangement, install its TOMLs and instructions, and adapt
it to your work. You do not need any private framework, MCP server or paid
third-party orchestration service to use these files.

[Guia em português](docs/README.pt-BR.md) ·
[Installation](docs/installation.md) · [Contributing](CONTRIBUTING.md) ·
[Orchestration rationale](docs/orchestration.md) ·
[Skills](skills/README.md) · [Plugins](plugins/README.md) ·
[Validation and compatibility](docs/validation.md)

Version 0.2.0 is a community preview. Historical hook and selected-role tests are
recorded; the revised allocations and caps are not fully runtime-certified.

## Choose an arrangement

| Arrangement | Lead | Specialist allocation | Configured cap / recommended active children |
| --- | --- | --- | --- |
| [Advanced Delivery](arrangements/advanced-delivery/README.md) | `gpt-5.6-sol`, `xhigh` | 15 roles: 4 Astra, 4 Sol, 7 Luna | 5 / up to 4 |
| [Balanced Delivery](arrangements/balanced-delivery/README.md) | `gpt-5.6-sol`, `xhigh` | 12 roles: 2 Astra, 2 Sol, 8 Luna | 4 / up to 3 |
| [Lean Delivery](arrangements/lean-delivery/README.md) | `gpt-5.6-sol`, `high` | 8 roles: 1 Astra, 1 Sol, 6 Luna | 3 / up to 2 |

The three arrangements provide progressively smaller role catalogs and enable
Multi-Agent V2. Roles are available choices, not agents started together. Allocate only useful,
independent work; parallel calls consume additional model tokens.

Advanced Delivery targets complex product work and spends more of its model
allocation on design, advice, critical review and coupled implementation.
Balanced Delivery reserves Astra for advice and coupled implementation, and Sol
for backend implementation and integration review. Lean Delivery uses Luna
broadly, keeps Astra for read-only advice, and uses Sol `high` to review integration
across deliveries. Lean backend and frontend implementation use Luna. If ambiguity or business risk exceeds the selected
role's capability, the lead reassesses the assignment before continuing.
These are routing objectives, not measured cost or quality guarantees; total
cost also depends on task length, retries and parallelism.

The explicit V2 cap includes the lead in the target runtime. The child
recommendations above reserve that slot. Recheck [compatibility evidence](docs/validation.md)
when upgrading the runtime or changing the cap's configuration field.

## What comes with an arrangement

- A small `config.toml` fragment and standalone `agents/*.toml` files.
- A self-contained AGENTS.md snippet, or a variant with inline triggers for the
  optional [codex-orchestration](skills/codex-orchestration/SKILL.md) and
  [pragmatic-programmer](skills/pragmatic-programmer/SKILL.md) skills.
- An optional [spawn-contract hook](hooks/spawn-contract/README.md) that checks
  explicit role selection and fresh-context delegation where the runtime
  intercepts spawn calls.
- A manifest describing the package, its author, license and runtime baseline.

Installation is manual. Merge only the documented settings into your existing
configuration; your credentials, permissions, tools and MCP configuration remain
your responsibility. Choosing an arrangement does not grant its agents new
permissions.

## Contribute your combination

Start with an existing arrangement, choose a distinct directory name, explain
the tradeoffs and include functional evidence. Skills, plugins and hooks are optional.
The [contribution guide](CONTRIBUTING.md) defines the package contract and checks.
Submit a pull request; do not upload your entire Codex home.

- [Propose an arrangement](https://github.com/rafaelob/fleet-codex/issues/new?template=new-arrangement.yml)
- [Report a correction](https://github.com/rafaelob/fleet-codex/issues/new?template=correction.yml)
- [Propose a skill, plugin or hook](https://github.com/rafaelob/fleet-codex/issues/new?template=new-component.yml)
- [Open a pull request](https://github.com/rafaelob/fleet-codex/compare)

You can contribute a new combination or improve an existing one. Public source,
configuration, instructions, issues and PRs use English; translated documentation
guides are welcome. See the [changelog](docs/CHANGELOG.md) for published changes.

## Share reusable workflow components

Components live outside the arrangements so they can serve any arrangement,
another community combination, or an existing workflow:

- [skills/](skills/README.md): standalone, optional skills, including
  `codex-orchestration` and `pragmatic-programmer`.
- [plugins/](plugins/README.md): independently contributed plugin packages that
  may bundle skills, public MCP configurations and hooks.
- [hooks/](hooks/spawn-contract/README.md): independently installable hook components.

The first release includes two skills and one standalone hook, not an installable
plugin bundle. Plugin contributions follow the official package format and need
their own installation and runtime evidence. No component is enabled by choosing
an arrangement.

## License

The catalog, agent configurations and hook are MIT licensed. The adapted
skills carry their own Apache-2.0 licenses and notices. Preserve
the applicable license files when redistributing components.
