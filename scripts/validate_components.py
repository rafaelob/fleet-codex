#!/usr/bin/env python3
"""Check public standalone skills and optional plugin package structure."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


PORTABLE_PLUGIN_SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
LICENSE_OR_PROVENANCE = (
    "LICENSE",
    "LICENSE.md",
    "LICENSE.txt",
    "NOTICE",
    "NOTICE.md",
    "PROVENANCE",
    "PROVENANCE.md",
)


@dataclass
class ComponentValidationResult:
    skills: int
    plugins: int
    errors: list[str]


def validate_components(catalog_root: Path | str) -> ComponentValidationResult:
    """Return local component counts and structural violations only."""

    errors: list[str] = []
    try:
        root = Path(catalog_root).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        return ComponentValidationResult(0, 0, [f"catalog root: cannot resolve {catalog_root}: {exc}"])
    if not root.is_dir():
        return ComponentValidationResult(0, 0, [f"catalog root: {root} is not a directory"])
    return ComponentValidationResult(
        _skills(root, root / "skills", root, "catalog root", errors),
        _plugins(root, errors),
        errors,
    )


def _plugins(root: Path, errors: list[str]) -> int:
    directory = root / "plugins"
    if not _present(directory, root, errors):
        return 0
    directory = _safe(root, directory, "plugins directory", "directory", "catalog root", errors)
    if directory is None:
        return 0
    try:
        entries = sorted(directory.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        errors.append(f"{_label(directory, root)}: cannot read plugin directory: {exc}")
        return 0

    count = 0
    for entry in entries:
        try:
            if not entry.is_dir():
                continue
        except OSError as exc:
            errors.append(f"{_label(entry, root)}: cannot inspect plugin entry: {exc}")
            continue
        count += 1
        plugin = _safe(
            root,
            entry,
            f"{_label(entry, root)}: plugin directory",
            "directory",
            "catalog root",
            errors,
        )
        if plugin is not None:
            _plugin(root, plugin, errors)
    return count


def _plugin(root: Path, plugin: Path, errors: list[str]) -> None:
    label = _label(plugin, root)
    _required_file(root, plugin, "README.md", errors)
    if not any(_present(plugin / name, root, errors) for name in LICENSE_OR_PROVENANCE):
        errors.append(f"{label}: requires a license or provenance file")
    else:
        for name in LICENSE_OR_PROVENANCE:
            if _present(plugin / name, root, errors):
                _safe(plugin, plugin / name, f"{label}: {name}", "file", "plugin directory", errors)
                break

    portable = _present(plugin / "plugin.json", root, errors)
    manifest_path = plugin / "plugin.json" if portable else plugin / ".codex-plugin" / "plugin.json"
    if not _present(manifest_path, root, errors):
        errors.append(f"{label}: has no plugin.json or .codex-plugin/plugin.json manifest")
        return
    manifest = _safe(
        plugin,
        manifest_path,
        f"{label}: {'plugin.json' if portable else '.codex-plugin/plugin.json'}",
        "file",
        "plugin directory",
        errors,
    )
    if manifest is None:
        return
    data = _json_object(manifest, root, errors)
    if data is None:
        return
    for field in ("name", "version", "description"):
        if not _text(data.get(field)):
            errors.append(f"{_label(manifest, root)}: manifest '{field}' must be a nonempty string")
    if _text(data.get("name")) and data["name"] != plugin.name:
        errors.append(f"{_label(manifest, root)}: manifest name must match plugin directory {plugin.name!r}")

    if portable:
        if data.get("$schema") != PORTABLE_PLUGIN_SCHEMA:
            errors.append(
                f"{_label(manifest, root)}: '$schema' must equal {PORTABLE_PLUGIN_SCHEMA!r}"
            )
        _portable(root, plugin, data, errors)
    else:
        _compatibility(root, plugin, data, errors)


def _portable(root: Path, plugin: Path, data: dict[str, Any], errors: list[str]) -> None:
    _skills(root, plugin / "skills", plugin, "plugin directory", errors)
    _optional_json(root, plugin, plugin / "mcp.json", "mcp.json", errors)

    settings, inline = _openai_settings(data, _label(plugin / "plugin.json", root), errors)
    source = "extensions.com.openai"
    if not inline:
        settings = _overlay(root, plugin, errors)
        source = ".codex-plugin/plugin.json"
    if settings is not None:
        _settings(root, plugin, settings, source, errors, allow_inline_mcp=True)
    if settings is None or "hooks" not in settings:
        _default_hooks(root, plugin, errors)


def _compatibility(root: Path, plugin: Path, data: dict[str, Any], errors: list[str]) -> None:
    if "skills" in data:
        skills = _reference(plugin, data["skills"], "compatibility manifest 'skills'", "directory", errors)
        if skills is not None:
            _skills(root, skills, plugin, "plugin directory", errors)
    else:
        _skills(root, plugin / "skills", plugin, "plugin directory", errors)
    _settings(root, plugin, data, "compatibility manifest", errors, allow_inline_mcp=True)
    if "hooks" not in data:
        _default_hooks(root, plugin, errors)


def _openai_settings(
    data: dict[str, Any], label: str, errors: list[str]
) -> tuple[dict[str, Any] | None, bool]:
    if "extensions" not in data:
        return None, False
    extensions = data["extensions"]
    if not isinstance(extensions, dict):
        errors.append(f"{label}: 'extensions' must be a JSON object when present")
        return None, True
    if "com.openai" not in extensions:
        return None, False
    settings = extensions["com.openai"]
    if not isinstance(settings, dict):
        errors.append(f"{label}: 'extensions.com.openai' must be a JSON object")
        return None, True
    return settings, True


def _overlay(root: Path, plugin: Path, errors: list[str]) -> dict[str, Any] | None:
    path = plugin / ".codex-plugin" / "plugin.json"
    if not _present(path, root, errors):
        return None
    path = _safe(
        plugin,
        path,
        f"{_label(plugin, root)}: .codex-plugin/plugin.json",
        "file",
        "plugin directory",
        errors,
    )
    return _json_object(path, root, errors) if path is not None else None


def _settings(
    root: Path,
    plugin: Path,
    data: dict[str, Any],
    label: str,
    errors: list[str],
    *,
    allow_inline_mcp: bool,
) -> None:
    if "apps" in data:
        _references(root, plugin, data["apps"], f"{label} 'apps'", "file", errors, json_file=True)
    if "mcpServers" in data and not (
        allow_inline_mcp and isinstance(data["mcpServers"], dict)
    ):
        _references(
            root,
            plugin,
            data["mcpServers"],
            f"{label} 'mcpServers'",
            "file",
            errors,
            json_file=True,
        )
    if "hooks" in data:
        values = data["hooks"] if isinstance(data["hooks"], list) else [data["hooks"]]
        for index, value in enumerate(values):
            suffix = f"[{index}]" if isinstance(data["hooks"], list) else ""
            if isinstance(value, dict):
                continue
            if not isinstance(value, str):
                errors.append(f"{label} 'hooks'{suffix}: must be a relative path or JSON object")
                continue
            path = _reference(plugin, value, f"{label} 'hooks'{suffix}", "file", errors)
            if path is not None:
                _json_object(path, root, errors)
    if "interface" in data:
        interface = data["interface"]
        if not isinstance(interface, dict):
            errors.append(f"{label} 'interface': must be a JSON object")
        else:
            for field in ("composerIcon", "logo", "logoDark", "screenshots"):
                if field in interface:
                    _references(
                        root,
                        plugin,
                        interface[field],
                        f"{label} 'interface' '{field}'",
                        "file",
                        errors,
                        json_file=False,
                    )


def _default_hooks(root: Path, plugin: Path, errors: list[str]) -> None:
    _optional_json(root, plugin, plugin / "hooks" / "hooks.json", "hooks/hooks.json", errors)


def _optional_json(root: Path, plugin: Path, path: Path, name: str, errors: list[str]) -> None:
    if not _present(path, root, errors):
        return
    path = _safe(
        plugin,
        path,
        f"{_label(plugin, root)}: {name}",
        "file",
        "plugin directory",
        errors,
    )
    if path is not None:
        _json_object(path, root, errors)


def _references(
    root: Path,
    plugin: Path,
    value: Any,
    label: str,
    kind: str,
    errors: list[str],
    *,
    json_file: bool,
) -> None:
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, list) and all(isinstance(item, str) for item in value):
        values = value
    else:
        errors.append(f"{label}: must be a relative path or list of relative paths")
        return
    for index, item in enumerate(values):
        suffix = f"[{index}]" if len(values) > 1 else ""
        path = _reference(plugin, item, f"{label}{suffix}", kind, errors)
        if json_file and path is not None:
            _json_object(path, root, errors)


def _skills(
    root: Path,
    directory: Path,
    boundary: Path,
    boundary_name: str,
    errors: list[str],
) -> int:
    if not _present(directory, root, errors):
        return 0
    directory = _safe(
        boundary,
        directory,
        f"{_label(directory, root)}: skills directory",
        "directory",
        boundary_name,
        errors,
    )
    if directory is None:
        return 0
    try:
        entries = sorted(directory.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        errors.append(f"{_label(directory, root)}: cannot read skills directory: {exc}")
        return 0
    count = 0
    for entry in entries:
        try:
            if not entry.is_dir():
                continue
        except OSError as exc:
            errors.append(f"{_label(entry, root)}: cannot inspect skill entry: {exc}")
            continue
        count += 1
        skill = _safe(
            boundary,
            entry,
            f"{_label(entry, root)}: skill directory",
            "directory",
            boundary_name,
            errors,
        )
        if skill is None:
            continue
        path = skill / "SKILL.md"
        if not _present(path, root, errors):
            errors.append(f"{_label(skill, root)}: requires SKILL.md")
            continue
        path = _safe(
            boundary,
            path,
            f"{_label(skill, root)}: SKILL.md",
            "file",
            boundary_name,
            errors,
        )
        if path is None:
            continue
        try:
            contents = path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"{_label(path, root)}: cannot read SKILL.md: {exc}")
            continue
        if not contents.strip():
            errors.append(f"{_label(path, root)}: must be nonempty")
    return count


def _required_file(root: Path, plugin: Path, name: str, errors: list[str]) -> None:
    path = plugin / name
    if not _present(path, root, errors):
        errors.append(f"{_label(plugin, root)}: requires {name}")
        return
    _safe(plugin, path, f"{_label(plugin, root)}: {name}", "file", "plugin directory", errors)


def _reference(plugin: Path, value: Any, label: str, kind: str, errors: list[str]) -> Path | None:
    if not _text(value):
        errors.append(f"{label}: must be a nonempty relative path")
        return None
    if _absolute(value):
        errors.append(f"{label}: must not be an absolute path")
        return None
    normalized = value.replace("\\", "/")
    if ".." in PurePosixPath(normalized).parts:
        errors.append(f"{label}: must not contain '..'")
        return None
    return _safe(plugin, plugin / Path(normalized), label, kind, "plugin directory", errors)


def _safe(
    boundary: Path,
    candidate: Path,
    label: str,
    kind: str,
    boundary_name: str,
    errors: list[str],
) -> Path | None:
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(boundary)
    except ValueError:
        errors.append(f"{label}: resolves outside {boundary_name}")
        return None
    except (OSError, RuntimeError) as exc:
        errors.append(f"{label}: cannot resolve {candidate}: {exc}")
        return None
    try:
        exists = candidate.exists()
        correct_kind = candidate.is_file() if kind == "file" else candidate.is_dir()
    except OSError as exc:
        errors.append(f"{label}: cannot inspect {candidate}: {exc}")
        return None
    if not exists:
        errors.append(f"{label}: does not exist")
        return None
    if not correct_kind:
        errors.append(f"{label}: must be a {kind}")
        return None
    try:
        return candidate.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        errors.append(f"{label}: cannot resolve {candidate}: {exc}")
        return None


def _json_object(path: Path, root: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        with path.open(encoding="utf-8") as source:
            data = json.load(source)
    except (json.JSONDecodeError, UnicodeError) as exc:
        errors.append(f"{_label(path, root)}: invalid JSON: {exc}")
        return None
    except OSError as exc:
        errors.append(f"{_label(path, root)}: cannot read JSON: {exc}")
        return None
    if not isinstance(data, dict):
        errors.append(f"{_label(path, root)}: JSON value must be an object")
        return None
    return data


def _present(path: Path, root: Path, errors: list[str]) -> bool:
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    except OSError as exc:
        errors.append(f"{_label(path, root)}: cannot inspect {path}: {exc}")
        return False
    return True


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _absolute(value: str) -> bool:
    windows = PureWindowsPath(value)
    return PurePosixPath(value).is_absolute() or bool(windows.drive or windows.root)


def _label(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    result = validate_components(parser.parse_args(argv).root)
    print(f"Components: skills={result.skills}, plugins={result.plugins}.")
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    if result.skills or result.plugins:
        print("Structural component preflight passed.")
    else:
        print("NOT APPLICABLE: no optional components were available to check.")
    print(
        "Limitations: this is not upstream-schema, security, command, network, "
        "or runtime-compatibility verification; SKILL.md frontmatter is not parsed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
