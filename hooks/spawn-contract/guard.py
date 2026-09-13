#!/usr/bin/env python3
"""Validate explicit-role, fresh-context spawn calls received by Codex hooks."""

import json
import sys


MAX_INPUT_BYTES = 1024 * 1024
SPAWN_NAMES = {"spawn_agent", "Agent", "agents.spawn_agent", "functions.spawn_agent",
               "agentsspawn_agent"}
OVERRIDES = {"model", "reasoning_effort", "model_reasoning_effort", "fork_context"}


def rejection(payload):
    if not isinstance(payload, dict):
        return "Spawn contract: expected a hook object."
    event = payload.get("hook_event_name")
    if not isinstance(event, str) or not event:
        return "Spawn contract: missing hook event."
    if event != "PreToolUse":
        return None
    tool = payload.get("tool_name")
    if not isinstance(tool, str) or not tool:
        return "Spawn contract: missing tool name."
    if tool not in SPAWN_NAMES:
        return None
    args = payload.get("tool_input")
    if not isinstance(args, dict):
        return "Spawn contract: expected structured spawn arguments."
    role = args.get("agent_type")
    if not isinstance(role, str) or not role.strip():
        return "Spawn contract: select an explicit agent_type from the available roles."
    if args.get("fork_turns") != "none":
        return 'Spawn contract: set fork_turns to "none" and put necessary context in the brief.'
    if OVERRIDES.intersection(args):
        return "Spawn contract: omit model/effort overrides and fork_context; use the role TOML."
    return None


def main():
    try:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            reason = "Spawn contract: hook input exceeds the size limit."
        else:
            reason = rejection(json.loads(raw))
    except (ValueError, UnicodeError, OSError, RecursionError):
        reason = "Spawn contract: unreadable or malformed hook input."
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
