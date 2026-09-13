import json
from pathlib import Path
import subprocess
import sys
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "hooks/spawn-contract/guard.py"


class SpawnContractTests(unittest.TestCase):
    def invoke(self, payload):
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT)],
            input=payload if isinstance(payload, str) else json.dumps(payload),
            text=True, capture_output=True, timeout=5,
        )

    def spawn(self, **overrides):
        args = {"agent_type": "explorer", "fork_turns": "none",
                "task_name": "map", "message": "Inspect the public interface."}
        args.update(overrides)
        return {"hook_event_name": "PreToolUse", "tool_name": "spawn_agent",
                "tool_input": args}

    def assert_denied(self, result):
        self.assertEqual(result.returncode, 0, result.stderr)
        decision = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertEqual(decision["permissionDecision"], "deny")
        self.assertTrue(decision["permissionDecisionReason"])

    def test_explicit_role_without_history_is_allowed_unchanged(self):
        result = self.invoke(self.spawn())
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "")

    def test_history_forks_are_denied(self):
        for value in (None, "all", "1", 1, "NONE", False):
            with self.subTest(value=value):
                self.assert_denied(self.invoke(self.spawn(fork_turns=value)))
        payload = self.spawn()
        del payload["tool_input"]["fork_turns"]
        self.assert_denied(self.invoke(payload))

    def test_missing_or_blank_role_is_denied(self):
        for value in (None, "", "  ", 3):
            self.assert_denied(self.invoke(self.spawn(agent_type=value)))
        payload = self.spawn()
        del payload["tool_input"]["agent_type"]
        self.assert_denied(self.invoke(payload))

    def test_call_level_model_and_effort_are_denied_even_when_null(self):
        for key in ("model", "reasoning_effort", "model_reasoning_effort"):
            self.assert_denied(self.invoke(self.spawn(**{key: None})))

    def test_old_fork_argument_is_denied(self):
        self.assert_denied(self.invoke(self.spawn(fork_context=True)))

    def test_known_tool_aliases_are_checked(self):
        for name in ("Agent", "agents.spawn_agent", "functions.spawn_agent", "agentsspawn_agent"):
            payload = self.spawn(fork_turns="all")
            payload["tool_name"] = name
            self.assert_denied(self.invoke(payload))

    def test_unrelated_tools_and_events_are_not_blocked(self):
        for name in ("Bash", "mcp__other__spawn_agent", "followup_task"):
            payload = self.spawn(fork_turns="all")
            payload["tool_name"] = name
            self.assertEqual(self.invoke(payload).stdout, "")
        payload = self.spawn(fork_turns="all")
        payload["hook_event_name"] = "PostToolUse"
        self.assertEqual(self.invoke(payload).stdout, "")

    def test_malformed_envelopes_are_denied_without_echoing_input(self):
        for payload in ("", "{secret:DO_NOT_ECHO}", "[]", "null",
                        {"hook_event_name": "PreToolUse"},
                        {"hook_event_name": "PreToolUse", "tool_name": "spawn_agent",
                         "tool_input": "DO_NOT_ECHO"}):
            result = self.invoke(payload)
            self.assert_denied(result)
            self.assertNotIn("DO_NOT_ECHO", result.stdout + result.stderr)

    def test_oversized_input_is_denied_without_processing(self):
        self.assert_denied(self.invoke(" " * (1024 * 1024 + 1)))


if __name__ == "__main__":
    unittest.main()
