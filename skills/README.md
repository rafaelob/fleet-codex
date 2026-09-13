# Optional workflow skills

Skills are independent of arrangement names and versions. Install only those
that help your work; neither initial arrangement requires one.

| Skill | Use it when |
| --- | --- |
| [codex-orchestration](codex-orchestration/SKILL.md) | Selecting a role, dispatching a bounded task, or reconciling deliveries |
| [pragmatic-programmer](pragmatic-programmer/SKILL.md) | Choosing a reversible design/change step, explaining a surprising green result, or checking shared knowledge, contracts and resource ownership |

## Install and invoke

Copy one complete skill directory, including its license and notice, into the
user or project skill location in the [installation guide](../docs/installation.md).
Verify the exact skill name appears in the runtime's available skills.

In Codex, an explicit user request can name `$pragmatic-programmer` or
`$codex-orchestration`. Agent-facing rules should tell the agent to invoke the
named skill through the runtime's Skill tool **if that tool exists**; otherwise
use the runtime's documented loading interface, including reading `SKILL.md`
when that is the exposed mechanism. Do not invent a `Skill(...)` API or treat
writing a name in a response as proof the skill loaded. See the
[official skills guide](https://developers.openai.com/codex/skills).

Use an arrangement's `AGENTS.with-skill.snippet.md` instead of its standalone
snippet. Its optional engineering section adds the contextual Pragmatic
Programmer trigger. Omit that section if you do not install the skill; the
orchestration section can be used independently. Preserve the fallback if a skill
may be absent in another installation. Do not paste a full skill into AGENTS.md.

## Contribute a skill

Add `skills/<skill-name>/SKILL.md` with valid `name` and `description` frontmatter;
the name must match its directory. Keep the description specific to the situations
that warrant loading the procedure. Put detailed references, scripts and assets
in their respective subdirectories only when needed. Include license/provenance
and any installation requirements without private paths or hidden dependencies.

Keep the always-loaded instruction trigger short and put detailed procedure in
the skill. Explain a positive use case and a similar situation that should not
trigger it. Validate the skill format with current authoring tools and exercise
the changed behavior; a prompt-only assessment is not an executable integration
test. Follow [Contributing](../CONTRIBUTING.md) for review and evidence.

If a plugin also distributes a skill from this catalog, declare its canonical
source and packaging step. Do not maintain two editable copies of the same skill
or make an installed plugin depend on files outside its package.
