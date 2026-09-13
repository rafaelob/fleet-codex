from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import validate_catalog


def build_catalog(root: Path, *, include_optional: bool = True) -> Path:
    arrangement = root / "arrangements" / "demo"
    agents = arrangement / "agents"
    agents.mkdir(parents=True)

    optional_fields = ""
    if include_optional:
        optional_fields = """\
instructions_with_skill = "AGENTS.with-skill.snippet.md"
optional_skills = ["../../skills/codex-orchestration"]
optional_hook = "../../hooks/spawn-contract"
"""

    (arrangement / "arrangement.toml").write_text(
        f"""\
schema_version = 1
id = "demo"
version = "1.0.0"
author = "Example Author"
description = "A public arrangement."
license = "MIT"
codex_version = ">=0.1"
config = "config.toml"
agents = "agents"
instructions = "AGENTS.snippet.md"
{optional_fields}""",
        encoding="utf-8",
    )
    (arrangement / "config.toml").write_text(
        """\
model = "example-model"
model_reasoning_effort = "medium"

[features]
multi_agent = true

[features.multi_agent_v2]
enabled = true
tool_namespace = "agents"
max_concurrent_threads_per_session = 4

[agents]
default_subagent_model = "example-model"
default_subagent_reasoning_effort = "medium"
""",
        encoding="utf-8",
    )
    (arrangement / "AGENTS.snippet.md").write_text(
        "Use the arrangement as documented.\n",
        encoding="utf-8",
    )
    (agents / "worker.toml").write_text(
        """\
name = "worker"
description = "Runs bounded work."
model = "example-model"
model_reasoning_effort = "medium"
developer_instructions = "Stay within the assigned boundary."
""",
        encoding="utf-8",
    )

    if include_optional:
        (arrangement / "AGENTS.with-skill.snippet.md").write_text(
            "Use the optional extension when it is installed.\n",
            encoding="utf-8",
        )
        skill = root / "skills" / "codex-orchestration"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "# Optional extension\n",
            encoding="utf-8",
        )
        hook = root / "hooks" / "spawn-contract"
        hook.mkdir(parents=True)
        (hook / "README.md").write_text(
            "Install the hook and run its entrypoint in the supported runtime.\n",
            encoding="utf-8",
        )
        (hook / "hook.js").write_text("export {};\n", encoding="utf-8")

    return arrangement


class CatalogValidatorTests(unittest.TestCase):
    def validate(self, root: Path) -> validate_catalog.ValidationResult:
        return validate_catalog.validate_catalog(root)

    def test_accepts_complete_catalog_and_reports_counts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build_catalog(root)

            result = self.validate(root)

            self.assertEqual([], result.errors)
            self.assertEqual(1, result.arrangements)
            self.assertEqual(1, result.roles)

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = validate_catalog.main(["--root", str(root)])
            self.assertEqual(0, exit_code)
            self.assertIn("1 arrangements, 1 roles", stdout.getvalue())
            self.assertEqual("", stderr.getvalue())

    def test_rejects_empty_catalog_with_nonzero_cli_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "arrangements").mkdir()

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = validate_catalog.main(["--root", str(root)])

            self.assertEqual(1, exit_code)
            self.assertIn("0 arrangements, 0 roles", stdout.getvalue())
            self.assertIn("no readable arrangements", stderr.getvalue())

    def test_reports_missing_manifest_reference(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            (arrangement / "AGENTS.snippet.md").unlink()

            errors = "\n".join(self.validate(root).errors)

            self.assertIn("'instructions' reference: does not exist", errors)

    def test_accepts_contained_community_component_references(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            manifest = arrangement / "arrangement.toml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    'config = "config.toml"',
                    'config = "community-config.toml"',
                ).replace(
                    'agents = "agents"',
                    'agents = "community-agents"',
                ).replace(
                    'instructions = "AGENTS.snippet.md"',
                    'instructions = "community.md"',
                ).replace(
                    'instructions_with_skill = "AGENTS.with-skill.snippet.md"',
                    'instructions_with_skill = "community.with-skill.md"',
                ).replace(
                    'optional_skills = ["../../skills/codex-orchestration"]',
                    'optional_skills = ["../../components/community-skill"]',
                ).replace(
                    'optional_hook = "../../hooks/spawn-contract"',
                    'optional_hook = "../../components/community-hook"',
                ),
                encoding="utf-8",
            )
            (arrangement / "community-config.toml").write_text(
                (arrangement / "config.toml").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            community_agents = arrangement / "community-agents"
            community_agents.mkdir()
            (community_agents / "worker.toml").write_text(
                (arrangement / "agents" / "worker.toml").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            (arrangement / "community.md").write_text("Community instructions.\n", encoding="utf-8")
            (arrangement / "community.with-skill.md").write_text(
                "Community extension instructions.\n",
                encoding="utf-8",
            )
            skill = root / "components" / "community-skill"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("# Community extension\n", encoding="utf-8")
            hook = root / "components" / "community-hook"
            hook.mkdir(parents=True)
            (hook / "README.md").write_text(
                "Install the hook and invoke entrypoint.sh with its shell runtime.\n",
                encoding="utf-8",
            )
            (hook / "entrypoint.sh").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")

            self.assertEqual([], self.validate(root).errors)

    def test_accepts_multiple_optional_skills(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            manifest = arrangement / "arrangement.toml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    'optional_skills = ["../../skills/codex-orchestration"]',
                    'optional_skills = ['
                    '"../../skills/codex-orchestration", '
                    '"../../components/second-skill"]',
                ),
                encoding="utf-8",
            )
            second_skill = root / "components" / "second-skill"
            second_skill.mkdir(parents=True)
            (second_skill / "SKILL.md").write_text("# Second skill\n", encoding="utf-8")

            self.assertEqual([], self.validate(root).errors)

    def test_rejects_invalid_optional_skills_and_legacy_alias(self) -> None:
        cases = (
            (
                'optional_skills = "../../skills/codex-orchestration"',
                "'optional_skills' must be a nonempty list of relative paths",
            ),
            (
                "optional_skills = []",
                "'optional_skills' must be a nonempty list of relative paths",
            ),
            (
                "optional_skills = [42]",
                "'optional_skills[0]' must be a nonempty relative path",
            ),
            (
                'optional_skill = "../../skills/codex-orchestration"',
                "'optional_skill' is unsupported; use 'optional_skills'",
            ),
        )
        source = 'optional_skills = ["../../skills/codex-orchestration"]'
        for replacement, expected_error in cases:
            with self.subTest(replacement=replacement), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                arrangement = build_catalog(root)
                manifest = arrangement / "arrangement.toml"
                manifest.write_text(
                    manifest.read_text(encoding="utf-8").replace(source, replacement),
                    encoding="utf-8",
                )

                self.assertIn(expected_error, "\n".join(self.validate(root).errors))

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            manifest = arrangement / "arrangement.toml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    'optional_skills = ["../../skills/codex-orchestration"]\n',
                    "",
                ),
                encoding="utf-8",
            )

            self.assertIn(
                "'instructions_with_skill' requires a nonempty 'optional_skills' list",
                "\n".join(self.validate(root).errors),
            )

    def test_reports_invalid_toml(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            (arrangement / "agents" / "worker.toml").write_text(
                "name = [\n",
                encoding="utf-8",
            )

            errors = "\n".join(self.validate(root).errors)

            self.assertIn("invalid TOML", errors)

    def test_rejects_reference_that_escapes_catalog_root(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            manifest = arrangement / "arrangement.toml"
            manifest.write_text(
                manifest.read_text(encoding="utf-8").replace(
                    'optional_skills = ["../../skills/codex-orchestration"]',
                    'optional_skills = ["../../../outside-skill"]',
                ).replace(
                    'optional_hook = "../../hooks/spawn-contract"',
                    'optional_hook = "../../../outside-hook"',
                ),
                encoding="utf-8",
            )

            errors = "\n".join(self.validate(root).errors)

            self.assertIn("'optional_skills[0]' reference: resolves outside catalog root", errors)
            self.assertIn("'optional_hook' reference: resolves outside catalog root", errors)

    def test_rejects_bad_config_types_and_disabled_v2(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            config = arrangement / "config.toml"
            config.write_text(
                config.read_text(encoding="utf-8")
                .replace("enabled = true", "enabled = false")
                .replace(
                    "max_concurrent_threads_per_session = 4",
                    "max_concurrent_threads_per_session = true",
                )
                .replace(
                    "[agents]\n",
                    "[agents]\nmax_concurrent_threads_per_session = 4\n",
                ),
                encoding="utf-8",
            )

            errors = "\n".join(self.validate(root).errors)

            self.assertIn("features.multi_agent_v2 'enabled' must be true", errors)
            self.assertIn(
                "features.multi_agent_v2 'max_concurrent_threads_per_session' "
                "must be a positive integer",
                errors,
            )

            config.write_text(
                config.read_text(encoding="utf-8") + '\nunsupported = "value"\n',
                encoding="utf-8",
            )
            self.assertIn(
                "agents has unsupported key 'unsupported'",
                "\n".join(self.validate(root).errors),
            )
            self.assertIn(
                "agents has unsupported key 'max_concurrent_threads_per_session'",
                "\n".join(self.validate(root).errors),
            )

    def test_rejects_missing_v2_thread_cap_and_allows_no_agents_table(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            config = arrangement / "config.toml"
            config.write_text(
                config.read_text(encoding="utf-8").replace(
                    "max_concurrent_threads_per_session = 4\n",
                    "",
                ),
                encoding="utf-8",
            )

            self.assertIn(
                "features.multi_agent_v2 is missing required key "
                "'max_concurrent_threads_per_session'",
                "\n".join(self.validate(root).errors),
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            config = arrangement / "config.toml"
            config.write_text(
                config.read_text(encoding="utf-8").replace(
                    "\n[agents]\ndefault_subagent_model = \"example-model\"\n"
                    "default_subagent_reasoning_effort = \"medium\"\n",
                    "\n",
                ),
                encoding="utf-8",
            )

            self.assertEqual([], self.validate(root).errors)

    def test_rejects_duplicate_and_mismatched_role_names(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            source = arrangement / "agents" / "worker.toml"
            (arrangement / "agents" / "other.toml").write_text(
                source.read_text(encoding="utf-8"),
                encoding="utf-8",
            )

            errors = "\n".join(self.validate(root).errors)

            self.assertIn("role filename must match name 'worker'", errors)
            self.assertIn("duplicate role name 'worker'", errors)

    def test_accepts_valid_english_nickname_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            role = arrangement / "agents" / "worker.toml"
            role.write_text(
                role.read_text(encoding="utf-8")
                + '\nnickname_candidates = ["Sunny Scout", "Bolt-Runner", "Atlas_2"]\n',
                encoding="utf-8",
            )

            self.assertEqual([], self.validate(root).errors)

    def test_rejects_invalid_nickname_candidates(self) -> None:
        cases = (
            (
                "nickname_candidates = []",
                "role 'nickname_candidates' must be a nonempty list of strings",
            ),
            (
                'nickname_candidates = "Sunny"',
                "role 'nickname_candidates' must be a nonempty list of strings",
            ),
            (
                "nickname_candidates = [42]",
                "nickname_candidates[0] must be a string",
            ),
            (
                'nickname_candidates = ["  "]',
                "nickname_candidates[0] must not be blank after trimming",
            ),
            (
                'nickname_candidates = ["Sunny", " Sunny "]',
                "nickname_candidates[1] duplicates 'Sunny' after trimming",
            ),
            (
                'nickname_candidates = ["Rafç"]',
                "nickname_candidates[0] contains unsupported characters",
            ),
            (
                'nickname_candidates = ["Lunã"]',
                "nickname_candidates[0] contains unsupported characters",
            ),
        )
        for nickname_toml, expected_error in cases:
            with self.subTest(nickname_toml=nickname_toml), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                arrangement = build_catalog(root)
                role = arrangement / "agents" / "worker.toml"
                role.write_text(
                    role.read_text(encoding="utf-8") + f"\n{nickname_toml}\n",
                    encoding="utf-8",
                )

                self.assertIn(expected_error, "\n".join(self.validate(root).errors))

    def test_optional_assets_are_optional_but_checked_when_declared(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            build_catalog(root, include_optional=False)
            self.assertEqual([], self.validate(root).errors)

            arrangement = build_catalog(root / "second")
            (arrangement.parent.parent / "skills" / "codex-orchestration" / "SKILL.md").unlink()
            (arrangement.parent.parent / "hooks" / "spawn-contract" / "README.md").unlink()

            errors = "\n".join(self.validate(arrangement.parent.parent).errors)

            self.assertIn("optional_skills[0] SKILL.md: does not exist", errors)
            self.assertIn("optional_hook README.md: does not exist", errors)

    def test_rejects_nonpublic_payload_contamination(self) -> None:
        cases = (
            ("~/.private-tool/state", "nonpublic hidden-home directory"),
            ("C:/Users/example/private", "personal user path"),
            ("/Users/example/private", "personal user path"),
            ("credentials.json", "credential filename"),
        )
        for payload, expected_error in cases:
            with self.subTest(payload=payload), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                arrangement = build_catalog(root)
                instructions = arrangement / "AGENTS.snippet.md"
                instructions.write_text(payload, encoding="utf-8")

                errors = "\n".join(self.validate(root).errors)

                self.assertIn(expected_error, errors)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            (arrangement / "AGENTS.snippet.md").write_text(
                "A public catalog name can contain ordinary words.\n",
                encoding="utf-8",
            )

            self.assertEqual([], self.validate(root).errors)

    def test_rejects_role_dependency_constructs_but_not_generic_prose(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            role = arrangement / "agents" / "worker.toml"
            role.write_text(
                role.read_text(encoding="utf-8").replace(
                    "Stay within the assigned boundary.",
                    "Inspect provider APIs and configuration before changing code.",
                ),
                encoding="utf-8",
            )

            self.assertEqual([], self.validate(root).errors)

            role.write_text(
                role.read_text(encoding="utf-8").replace(
                    "Inspect provider APIs and configuration before changing code.",
                    "Read ~/.codex/skills/codex-orchestration/SKILL.md.",
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "dependency/config reference '.codex/skills/'",
                "\n".join(self.validate(root).errors),
            )

            role.write_text(
                role.read_text(encoding="utf-8") + '\n[mcp]\nserver = "local"\n',
                encoding="utf-8",
            )
            self.assertIn(
                "role has unsupported key 'mcp'",
                "\n".join(self.validate(root).errors),
            )

    def test_invalid_utf8_toml_returns_nonzero_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            arrangement = build_catalog(root)
            (arrangement / "config.toml").write_bytes(b"\xff")

            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = validate_catalog.main(["--root", str(root)])

            self.assertEqual(1, exit_code)
            self.assertIn("invalid TOML", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
