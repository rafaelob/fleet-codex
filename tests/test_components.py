from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "scripts"))

import validate_components


PORTABLE_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def write_skill(directory: Path, name: str = "helper") -> None:
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: A reusable helper.\n---\n\n# Helper\n",
        encoding="utf-8",
    )


def portable_manifest(name: str) -> dict[str, object]:
    return {
        "$schema": PORTABLE_SCHEMA,
        "name": name,
        "version": "1.0.0",
        "description": "A portable test plugin.",
    }


def compatibility_manifest(name: str) -> dict[str, object]:
    return {
        "name": name,
        "version": "1.0.0",
        "description": "A compatibility test plugin.",
    }


def create_plugin(root: Path, name: str, *, portable: bool) -> Path:
    plugin = root / "plugins" / name
    plugin.mkdir(parents=True)
    (plugin / "README.md").write_text("# Plugin\n", encoding="utf-8")
    (plugin / "LICENSE").write_text("MIT\n", encoding="utf-8")
    manifest = portable_manifest(name) if portable else compatibility_manifest(name)
    manifest_path = plugin / "plugin.json"
    if not portable:
        manifest_path = plugin / ".codex-plugin" / "plugin.json"
    write_json(manifest_path, manifest)
    return plugin


def link_directory(link: Path, target: Path) -> None:
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError as exc:
        if os.name != "nt":
            raise
        environment = os.environ.copy()
        environment.update(CATALOG_TEST_LINK=str(link), CATALOG_TEST_TARGET=str(target))
        subprocess.run(
            ["pwsh", "-NoLogo", "-NoProfile", "-NonInteractive", "-Command",
             "New-Item -ItemType Junction -Path $env:CATALOG_TEST_LINK "
             "-Target $env:CATALOG_TEST_TARGET -ErrorAction Stop | Out-Null"],
            env=environment, check=True, capture_output=True, timeout=15,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        if link.resolve() != target.resolve():
            raise RuntimeError("Directory-link fixture did not resolve to its target") from exc


class ComponentValidatorTests(unittest.TestCase):
    def validate(self, root: Path) -> validate_components.ComponentValidationResult:
        return validate_components.validate_components(root)

    def test_unreadable_component_collection_is_reported_as_error(self) -> None:
        original_lstat = Path.lstat
        for component in ("skills", "plugins"):
            with self.subTest(component=component), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary).resolve()
                inaccessible = root / component
                inaccessible.mkdir()

                def deny(path: Path):
                    if path == inaccessible:
                        raise PermissionError("permission denied")
                    return original_lstat(path)

                stdout = io.StringIO()
                stderr = io.StringIO()
                with mock.patch.object(Path, "lstat", autospec=True, side_effect=deny):
                    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                        exit_code = validate_components.main(["--root", str(root)])

                self.assertEqual(1, exit_code)
                self.assertIn(f"{component}: cannot inspect", stderr.getvalue())
                self.assertNotIn("NOT APPLICABLE", stdout.getvalue())

    def test_readme_only_reports_zero_plugins(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text("# Catalog\n", encoding="utf-8")
            (root / "plugins").mkdir()
            (root / "plugins" / "README.md").write_text("# Plugins\n", encoding="utf-8")

            result = self.validate(root)

            self.assertEqual([], result.errors)
            self.assertEqual(0, result.skills)
            self.assertEqual(0, result.plugins)
            stdout = io.StringIO()
            stderr = io.StringIO()
            with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
                exit_code = validate_components.main(["--root", str(root)])
            self.assertEqual(0, exit_code)
            self.assertIn("plugins=0", stdout.getvalue())
            self.assertNotIn("preflight passed", stdout.getvalue())
            self.assertEqual("", stderr.getvalue())

    def test_accepts_portable_plugin_with_optional_components(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = create_plugin(root, "portable", portable=True)
            manifest = portable_manifest("portable")
            manifest["extensions"] = {
                "com.openai": {
                    "apps": "./.app.json",
                    "hooks": "./hooks/custom.json",
                    "interface": {
                        "logo": "./assets/logo.svg",
                        "logoDark": "./assets/logo-dark.svg",
                        "screenshots": ["./assets/example.png"],
                    },
                }
            }
            write_json(plugin / "plugin.json", manifest)
            write_json(plugin / ".app.json", {"apps": {}})
            write_json(
                plugin / "mcp.json",
                {"mcpServers": {"demo": {"type": "streamable-http"}}},
            )
            write_json(plugin / "hooks" / "custom.json", {"hooks": {}})
            write_skill(plugin / "skills" / "helper")
            (plugin / "assets").mkdir()
            (plugin / "assets" / "logo.svg").write_text("<svg />", encoding="utf-8")
            (plugin / "assets" / "logo-dark.svg").write_text("<svg />", encoding="utf-8")
            (plugin / "assets" / "example.png").write_bytes(b"PNG")

            result = self.validate(root)

            self.assertEqual([], result.errors)
            self.assertEqual(0, result.skills)
            self.assertEqual(1, result.plugins)

    def test_accepts_compatibility_plugin_with_optional_components(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = create_plugin(root, "compat", portable=False)
            manifest = compatibility_manifest("compat")
            manifest.update(
                {
                    "skills": "./skills",
                    "mcpServers": "./.mcp.json",
                    "apps": "./.app.json",
                    "hooks": "./hooks/hooks.json",
                    "interface": {"logo": "./assets/logo.svg"},
                }
            )
            write_json(plugin / ".codex-plugin" / "plugin.json", manifest)
            write_skill(plugin / "skills" / "helper")
            write_json(plugin / ".mcp.json", {"mcpServers": {}})
            write_json(plugin / ".app.json", {"apps": {}})
            write_json(plugin / "hooks" / "hooks.json", {"hooks": {}})
            (plugin / "assets").mkdir()
            (plugin / "assets" / "logo.svg").write_text("<svg />", encoding="utf-8")

            self.assertEqual([], self.validate(root).errors)

    def test_portable_manifest_wins_over_compatibility_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = create_plugin(root, "portable", portable=True)
            manifest = portable_manifest("portable")
            manifest["extensions"] = {"com.openai": {}}
            write_json(plugin / "plugin.json", manifest)
            compatibility = plugin / ".codex-plugin" / "plugin.json"
            compatibility.parent.mkdir()
            compatibility.write_text("not JSON", encoding="utf-8")

            self.assertEqual([], self.validate(root).errors)

    def test_portable_root_uses_compatibility_overlay_without_inline_settings(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = create_plugin(root, "portable", portable=True)
            write_json(
                plugin / ".codex-plugin" / "plugin.json",
                {"hooks": "./hooks/missing.json"},
            )

            self.assertIn("does not exist", "\n".join(self.validate(root).errors))

    def test_rejects_missing_manifest_and_required_plugin_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = root / "plugins" / "missing"
            plugin.mkdir(parents=True)
            (plugin / "README.md").write_text("# Plugin\n", encoding="utf-8")
            (plugin / "LICENSE").write_text("MIT\n", encoding="utf-8")

            self.assertIn(
                "has no plugin.json or .codex-plugin/plugin.json manifest",
                "\n".join(self.validate(root).errors),
            )

        for missing_name, expected_error in (
            ("README.md", "requires README.md"),
            ("LICENSE", "requires a license or provenance file"),
        ):
            with self.subTest(missing_name=missing_name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                plugin = create_plugin(root, "required", portable=True)
                (plugin / missing_name).unlink()

                self.assertIn(expected_error, "\n".join(self.validate(root).errors))

    def test_rejects_invalid_manifest_identity_and_json_companions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = create_plugin(root, "identity", portable=True)
            manifest = portable_manifest("other")
            manifest["version"] = " "
            manifest["$schema"] = "https://agent-plugins.org/schemas/not-supported.json"
            write_json(plugin / "plugin.json", manifest)
            (plugin / "mcp.json").write_text("[]", encoding="utf-8")

            errors = "\n".join(self.validate(root).errors)

            self.assertIn("manifest name must match plugin directory 'identity'", errors)
            self.assertIn("manifest 'version' must be a nonempty string", errors)
            self.assertIn("'$schema' must equal", errors)
            self.assertIn("mcp.json: JSON value must be an object", errors)

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = create_plugin(root, "malformed", portable=True)
            (plugin / "plugin.json").write_text("{", encoding="utf-8")

            self.assertIn("plugin.json: invalid JSON", "\n".join(self.validate(root).errors))

    def test_rejects_unsafe_or_missing_companion_references(self) -> None:
        cases = (
            ("hooks", "../outside.json", "must not contain '..'"),
            ("apps", "C:/outside.json", "must not be an absolute path"),
            ("hooks", "./hooks/missing.json", "does not exist"),
        )
        for field, value, expected_error in cases:
            with self.subTest(field=field, value=value), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                plugin = create_plugin(root, "unsafe", portable=True)
                manifest = portable_manifest("unsafe")
                manifest["extensions"] = {"com.openai": {field: value}}
                write_json(plugin / "plugin.json", manifest)

                self.assertIn(expected_error, "\n".join(self.validate(root).errors))

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = create_plugin(root, "symlink", portable=True)
            outside = root / "outside"
            outside.mkdir()
            (outside / "escape.json").write_text("{}", encoding="utf-8")
            link = plugin / "hooks" / "escape"
            link.parent.mkdir()
            link_directory(link, outside)
            manifest = portable_manifest("symlink")
            manifest["extensions"] = {"com.openai": {"hooks": "./hooks/escape/escape.json"}}
            write_json(plugin / "plugin.json", manifest)

            self.assertIn(
                "resolves outside plugin directory",
                "\n".join(self.validate(root).errors),
            )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = create_plugin(root, "asset", portable=True)
            manifest = portable_manifest("asset")
            manifest["extensions"] = {
                "com.openai": {"interface": {"logoDark": "./assets/missing.svg"}}
            }
            write_json(plugin / "plugin.json", manifest)

            self.assertIn("does not exist", "\n".join(self.validate(root).errors))

    def test_compatibility_defaults_and_inline_mcp_are_structurally_checked(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plugin = create_plugin(root, "compat", portable=False)
            write_json(
                plugin / ".codex-plugin" / "plugin.json",
                {"name": "compat", "version": "1.0.0", "description": "Compatibility.",
                 "mcpServers": {"local": {"command": "never-executed"}}},
            )
            skill = plugin / "skills" / "empty"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("", encoding="utf-8")
            write_json(plugin / "hooks" / "hooks.json", [])

            errors = "\n".join(self.validate(root).errors)

            self.assertIn("SKILL.md: must be nonempty", errors)
            self.assertIn("hooks.json: JSON value must be an object", errors)
            self.assertNotIn("mcpServers': must be a relative path", errors)

    def test_validates_nonempty_standalone_skill_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_skill(root / "skills" / "valid", "valid")
            broken = root / "skills" / "broken"
            broken.mkdir()
            (broken / "SKILL.md").write_text("", encoding="utf-8")

            result = self.validate(root)

            self.assertEqual(2, result.skills)
            self.assertIn(
                "SKILL.md: must be nonempty",
                "\n".join(result.errors),
            )


if __name__ == "__main__":
    unittest.main()
