#!/usr/bin/env python3
"""Validate the public arrangement catalog with Python's standard library."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any


MANIFEST_TEXT_FIELDS = {
    "id",
    "version",
    "author",
    "description",
    "license",
    "codex_version",
}
ROLE_FIELDS = {
    "name",
    "description",
    "model",
    "model_reasoning_effort",
    "developer_instructions",
}
ROLE_ALLOWED_FIELDS = ROLE_FIELDS | {"nickname_candidates"}
NICKNAME_CANDIDATE_PATTERN = re.compile(r"^[A-Za-z0-9 _-]+$")
CONFIG_FIELDS = {"model", "model_reasoning_effort", "features", "agents"}
FEATURE_FIELDS = {"multi_agent", "multi_agent_v2"}
V2_FIELDS = {
    "enabled",
    "tool_namespace",
    "max_concurrent_threads_per_session",
}
# Effective defaults in the catalog's pinned Codex V2 baseline.
WAIT_DEFAULTS = {
    "min_wait_timeout_ms": 10_000,
    "default_wait_timeout_ms": 30_000,
    "max_wait_timeout_ms": 3_600_000,
}
AGENT_FIELDS = {
    "default_subagent_model",
    "default_subagent_reasoning_effort",
}
NONPUBLIC_PAYLOAD_PATTERNS = (
    (
        re.compile(
            r"(?:~|\$HOME|%USERPROFILE%)[\\/]"
            r"\.(?!(?:codex|agents)(?:[\\/]|$))[A-Za-z0-9_.-]+(?:[\\/]|$)",
            re.IGNORECASE,
        ),
        "nonpublic hidden-home directory",
    ),
    (
        re.compile(r"(?:[A-Z]:[\\/]|/)[\\/]?users[\\/]", re.IGNORECASE),
        "personal user path",
    ),
    (
        re.compile(
            r"""(?ix)
            (?:^|[\\/])
            (?:
                \.env(?:\.[A-Za-z0-9_.-]+)?
                |credentials?(?:\.[A-Za-z0-9_.-]+)?
                |id_(?:rsa|ecdsa|ed25519)
                |[A-Za-z0-9_.-]*(?:token|secret|api[_-]?key)[A-Za-z0-9_.-]*
                    \.(?:json|toml|ya?ml|env)
            )
            (?=$|[\\/\s"',.)])
            """
        ),
        "credential filename",
    ),
)
ROLE_DEPENDENCY_PATTERN = re.compile(
    r"""
    (?:\.(?:codex|agents)[\\/](?:skills|plugins)[\\/])
    |(?:\b(?:skills|plugins)[\\/][A-Za-z0-9_.-]+)
    |(?:\b(?:mcp|providers?|skills?|plugins?)\.(?:json|toml|ya?ml)\b)
    |(?:\b(?:mcp|provider|skill|plugin)_(?:config|server|path|name)\b)
    |(?:\bconfig\.toml\b)
    """,
    re.IGNORECASE | re.VERBOSE,
)


@dataclass
class ValidationResult:
    arrangements: int
    roles: int
    errors: list[str]


def validate_catalog(catalog_root: Path | str) -> ValidationResult:
    """Return catalog counts and all deterministic contract violations."""

    errors: list[str] = []
    scanned: set[Path] = set()
    try:
        root = Path(catalog_root).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        errors.append(f"catalog root: cannot resolve {catalog_root}: {exc}")
        return ValidationResult(0, 0, errors)
    if not root.is_dir():
        errors.append(f"catalog root: {root} is not a directory")
        return ValidationResult(0, 0, errors)

    arrangements_dir = _path(
        root,
        root / "arrangements",
        "arrangements directory",
        "directory",
        errors,
    )
    if arrangements_dir is None:
        return ValidationResult(0, 0, errors)
    try:
        entries = sorted(arrangements_dir.iterdir(), key=lambda item: item.name)
    except OSError as exc:
        errors.append(
            f"{_label(arrangements_dir, root)}: cannot read arrangement directory: {exc}"
        )
        return ValidationResult(0, 0, errors)

    arrangements = 0
    roles = 0
    for entry in entries:
        try:
            is_directory = entry.is_dir()
        except OSError as exc:
            errors.append(f"arrangement entry {entry}: cannot inspect: {exc}")
            continue
        if not is_directory:
            continue

        arrangement_dir = _path(root, entry, "arrangement directory", "directory", errors)
        if arrangement_dir is None:
            continue
        manifest = _path(
            root,
            arrangement_dir / "arrangement.toml",
            "arrangement manifest",
            "file",
            errors,
        )
        if manifest is None:
            continue
        arrangements += 1

        data = _read_toml(manifest, root, errors)
        if data is None:
            continue
        _scan(manifest, root, scanned, errors)
        roles += _validate_arrangement(
            root,
            entry.name,
            manifest,
            data,
            scanned,
            errors,
        )

    if arrangements == 0:
        errors.append("catalog has no readable arrangements/<id>/arrangement.toml files")
    return ValidationResult(arrangements, roles, errors)


def _validate_arrangement(
    root: Path,
    directory_name: str,
    manifest: Path,
    data: dict[str, Any],
    scanned: set[Path],
    errors: list[str],
) -> int:
    label = _label(manifest, root)
    if type(data.get("schema_version")) is not int or data.get("schema_version") != 1:
        errors.append(f"{label}: 'schema_version' must be the integer 1")
    for field in sorted(MANIFEST_TEXT_FIELDS):
        if not _text(data.get(field)):
            errors.append(f"{label}: '{field}' must be a nonempty string")
    if _text(data.get("id")) and data["id"] != directory_name:
        errors.append(f"{label}: 'id' must match its arrangement directory ({directory_name!r})")
    config = _reference(root, manifest, data.get("config"), "config", "file", errors)
    agents = _reference(root, manifest, data.get("agents"), "agents", "directory", errors)
    instructions = _reference(
        root,
        manifest,
        data.get("instructions"),
        "instructions",
        "file",
        errors,
    )
    for path in (config, instructions):
        if path is not None:
            _scan(path, root, scanned, errors)

    if "optional_skill" in data:
        errors.append(f"{label}: 'optional_skill' is unsupported; use 'optional_skills'")
    optional_skills = data.get("optional_skills")
    with_skill = data.get("instructions_with_skill")
    if optional_skills is None:
        if with_skill is not None:
            errors.append(
                f"{label}: 'instructions_with_skill' requires a nonempty "
                "'optional_skills' list"
            )
    elif not isinstance(optional_skills, list) or not optional_skills:
        errors.append(f"{label}: 'optional_skills' must be a nonempty list of relative paths")
        if with_skill is not None:
            errors.append(
                f"{label}: 'instructions_with_skill' requires a nonempty "
                "'optional_skills' list"
            )
    else:
        for index, optional_skill in enumerate(optional_skills):
            skill_dir = _reference(
                root,
                manifest,
                optional_skill,
                f"optional_skills[{index}]",
                "directory",
                errors,
            )
            if skill_dir is not None:
                skill_file = _path(
                    root,
                    skill_dir / "SKILL.md",
                    f"{label}: optional_skills[{index}] SKILL.md",
                    "file",
                    errors,
                )
                if skill_file is not None:
                    _scan(skill_file, root, scanned, errors)
        if with_skill is not None:
            skill_instructions = _reference(
                root,
                manifest,
                with_skill,
                "instructions_with_skill",
                "file",
                errors,
            )
            if skill_instructions is not None:
                _scan(skill_instructions, root, scanned, errors)

    if data.get("optional_hook") is not None:
        hook_dir = _reference(
            root,
            manifest,
            data["optional_hook"],
            "optional_hook",
            "directory",
            errors,
        )
        if hook_dir is not None:
            hook_readme = _path(
                root,
                hook_dir / "README.md",
                f"{label}: optional_hook README.md",
                "file",
                errors,
            )
            if hook_readme is not None:
                _scan(hook_readme, root, scanned, errors)

    if config is not None:
        config_data = _read_toml(config, root, errors)
        if config_data is not None:
            _validate_config(config, root, config_data, errors)
    return _validate_roles(agents, root, scanned, errors) if agents is not None else 0


def _validate_config(path: Path, root: Path, data: dict[str, Any], errors: list[str]) -> None:
    label = _label(path, root)
    _keys(data, CONFIG_FIELDS, label, "config", errors, required=CONFIG_FIELDS - {"agents"})
    for field in ("model", "model_reasoning_effort"):
        if not _text(data.get(field)):
            errors.append(f"{label}: config '{field}' must be a nonempty string")

    features = data.get("features")
    if not isinstance(features, dict):
        errors.append(f"{label}: config 'features' must be a table")
    else:
        _keys(features, FEATURE_FIELDS, label, "features", errors)
        if type(features.get("multi_agent")) is not bool:
            errors.append(f"{label}: features 'multi_agent' must be a boolean")
        v2 = features.get("multi_agent_v2")
        if not isinstance(v2, dict):
            errors.append(f"{label}: features 'multi_agent_v2' must be a table")
        else:
            _keys(
                v2, V2_FIELDS | WAIT_DEFAULTS.keys(), label,
                "features.multi_agent_v2", errors, required=V2_FIELDS,
            )
            if v2.get("enabled") is not True:
                errors.append(f"{label}: features.multi_agent_v2 'enabled' must be true")
            if not _text(v2.get("tool_namespace")):
                errors.append(
                    f"{label}: features.multi_agent_v2 'tool_namespace' must be a nonempty string"
                )
            capacity = v2.get("max_concurrent_threads_per_session")
            if type(capacity) is not int or capacity <= 0:
                errors.append(
                    f"{label}: features.multi_agent_v2 "
                    "'max_concurrent_threads_per_session' must be a positive integer"
                )
            waits = {field: v2.get(field, default) for field, default in WAIT_DEFAULTS.items()}
            invalid_waits = [
                field for field, value in waits.items()
                if type(value) is not int or not 0 <= value <= 3_600_000
            ]
            for field in invalid_waits:
                errors.append(
                    f"{label}: wait timeout '{field}' must be an integer from 0 to 3600000"
                )
            if not invalid_waits and not (
                waits["min_wait_timeout_ms"]
                <= waits["default_wait_timeout_ms"]
                <= waits["max_wait_timeout_ms"]
            ):
                errors.append(
                    f"{label}: effective wait timeouts must satisfy minimum <= default <= maximum"
                )

    agents = data.get("agents")
    if agents is None:
        return
    if not isinstance(agents, dict):
        errors.append(f"{label}: config 'agents' must be a table")
        return
    _keys(agents, AGENT_FIELDS, label, "agents", errors, required=set())
    for field in (
        "default_subagent_model",
        "default_subagent_reasoning_effort",
    ):
        if field in agents and not _text(agents[field]):
            errors.append(f"{label}: agents '{field}' must be a nonempty string when present")


def _validate_roles(
    agents_dir: Path,
    root: Path,
    scanned: set[Path],
    errors: list[str],
) -> int:
    try:
        candidates = sorted(agents_dir.glob("*.toml"), key=lambda item: item.name)
    except OSError as exc:
        errors.append(f"{_label(agents_dir, root)}: cannot read role TOMLs: {exc}")
        return 0
    if not candidates:
        errors.append(f"{_label(agents_dir, root)}: contains no role TOML files")
        return 0

    names: set[str] = set()
    for candidate in candidates:
        path = _path(root, candidate, "role TOML", "file", errors)
        if path is None:
            continue
        _scan(path, root, scanned, errors)
        role = _read_toml(path, root, errors)
        if role is None:
            continue

        label = _label(path, root)
        _keys(role, ROLE_ALLOWED_FIELDS, label, "role", errors, required=ROLE_FIELDS)
        for field in sorted(ROLE_FIELDS):
            if not _text(role.get(field)):
                errors.append(f"{label}: role '{field}' must be a nonempty string")
        nickname_candidates = role.get("nickname_candidates")
        if "nickname_candidates" in role:
            if not isinstance(nickname_candidates, list) or not nickname_candidates:
                errors.append(
                    f"{label}: role 'nickname_candidates' must be a nonempty list of strings"
                )
            else:
                seen_candidates: set[str] = set()
                for index, nickname_candidate in enumerate(nickname_candidates):
                    if not isinstance(nickname_candidate, str):
                        errors.append(
                            f"{label}: nickname_candidates[{index}] must be a string"
                        )
                        continue
                    normalized_candidate = nickname_candidate.strip()
                    if not normalized_candidate:
                        errors.append(
                            f"{label}: nickname_candidates[{index}] "
                            "must not be blank after trimming"
                        )
                        continue
                    if normalized_candidate in seen_candidates:
                        errors.append(
                            f"{label}: nickname_candidates[{index}] duplicates "
                            f"{normalized_candidate!r} after trimming"
                        )
                    seen_candidates.add(normalized_candidate)
                    if NICKNAME_CANDIDATE_PATTERN.fullmatch(normalized_candidate) is None:
                        errors.append(
                            f"{label}: nickname_candidates[{index}] "
                            "contains unsupported characters"
                        )
        name = role.get("name")
        if _text(name):
            if path.stem != name:
                errors.append(f"{label}: role filename must match name {name!r}")
            if name in names:
                errors.append(f"{label}: duplicate role name {name!r}")
            names.add(name)
        for field, value in role.items():
            if not isinstance(value, str):
                continue
            match = ROLE_DEPENDENCY_PATTERN.search(value)
            if match is not None:
                errors.append(
                    f"{label}: role '{field}' contains dependency/config reference "
                    f"{match.group(0)!r}"
                )
    return len(candidates)


def _keys(
    data: dict[str, Any],
    allowed: set[str],
    label: str,
    section: str,
    errors: list[str],
    *,
    required: set[str] | None = None,
) -> None:
    required = allowed if required is None else required
    for field in sorted(required - data.keys()):
        errors.append(f"{label}: {section} is missing required key {field!r}")
    for field in sorted(data.keys() - allowed):
        errors.append(f"{label}: {section} has unsupported key {field!r}")


def _reference(
    root: Path,
    manifest: Path,
    value: Any,
    field: str,
    kind: str,
    errors: list[str],
) -> Path | None:
    label = _label(manifest, root)
    if not _text(value):
        errors.append(f"{label}: '{field}' must be a nonempty relative path")
        return None
    if _absolute(value):
        errors.append(f"{label}: '{field}' must not be an absolute path")
        return None
    candidate = manifest.parent / Path(value.replace("\\", "/"))
    return _path(root, candidate, f"{label}: '{field}' reference", kind, errors)


def _path(
    root: Path,
    candidate: Path,
    description: str,
    kind: str,
    errors: list[str],
) -> Path | None:
    try:
        resolved = candidate.resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        errors.append(f"{description}: cannot resolve {candidate}: {exc}")
        return None
    try:
        resolved.relative_to(root)
    except ValueError:
        errors.append(f"{description}: resolves outside catalog root")
        return None

    try:
        exists = candidate.exists()
        matches_kind = candidate.is_file() if kind == "file" else candidate.is_dir()
    except OSError as exc:
        errors.append(f"{description}: cannot inspect {candidate}: {exc}")
        return None
    if not exists:
        errors.append(f"{description}: does not exist")
        return None
    if not matches_kind:
        errors.append(f"{description}: must be a {kind}")
        return None
    try:
        return candidate.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        errors.append(f"{description}: cannot resolve {candidate}: {exc}")
        return None


def _read_toml(path: Path, root: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        with path.open("rb") as source:
            return tomllib.load(source)
    except (tomllib.TOMLDecodeError, UnicodeError) as exc:
        errors.append(f"{_label(path, root)}: invalid TOML: {exc}")
    except OSError as exc:
        errors.append(f"{_label(path, root)}: cannot read TOML: {exc}")
    return None


def _scan(path: Path, root: Path, scanned: set[Path], errors: list[str]) -> None:
    if path in scanned:
        return
    scanned.add(path)
    try:
        payload = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        errors.append(f"{_label(path, root)}: public payload is not UTF-8 readable: {exc}")
        return
    for pattern, description in NONPUBLIC_PAYLOAD_PATTERNS:
        match = pattern.search(payload)
        if match is not None:
            line = payload.count("\n", 0, match.start()) + 1
            errors.append(f"{_label(path, root)}:{line}: public payload contains {description}")


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _absolute(value: str) -> bool:
    windows = PureWindowsPath(value)
    return PurePosixPath(value).is_absolute() or bool(windows.drive or windows.root)


def _label(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root).as_posix()
    except (OSError, RuntimeError, ValueError):
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the public arrangement catalog.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="catalog root (defaults to the repository root)",
    )
    result = validate_catalog(parser.parse_args(argv).root)
    print(f"Catalog: {result.arrangements} arrangements, {result.roles} roles.")
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Catalog validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
