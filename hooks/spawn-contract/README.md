# Optional spawn contract

This command hook checks the arguments of intercepted Codex spawn calls. It is
independent of the arrangement's agent files and optional to install.

It allows an explicit nonblank `agent_type` with `fork_turns: "none"`. It denies
missing roles, history forks, `fork_context`, and call-level `model`,
`reasoning_effort` or `model_reasoning_effort` fields. Models and efforts belong
in the selected role's TOML. It does not rewrite the task or the message.

The hook does not validate model quality, inspect task content, grant permissions,
verify that a role exists, count threads, or detect whether the caller is a child.
Only-the-lead-delegates remains an instruction. Unrelated tools are left alone.

## Install and review

1. Install Python 3.11+ if needed. Copy `guard.py` to a stable local directory.
2. Adapt `hooks.example.json`: replace the Python command and script placeholder
   with the real paths on your machine. Use a quoted absolute script path; on
   Windows, forward slashes in JSON avoid unnecessary escaping. For example,
   `python -X utf8 "/path with spaces/spawn-contract/guard.py"`.
3. Merge the `PreToolUse` group into your user or trusted project `hooks.json`.
   Preserve existing hooks. Do not use the example's placeholder literally.
4. Merge `hooks = true` into `[features]` in that scope's `config.toml` if it is
   not already enabled. Restart Codex, open `/hooks`, inspect the script and
   command, and trust this exact definition.
5. Run the tests and real integration check below. A changed definition requires
   review again; do not reuse another installation's trust hash.

No hook is installed automatically by copying an arrangement. No trust bypass
is part of the installation procedure.

## Contract and tests

Input is one JSON object on standard input. The handler has no arguments,
external dependencies, network calls or persistent log. The example runtime
timeout is five seconds and input is bounded to one MiB. Denials are returned as
`hookSpecificOutput.permissionDecision = "deny"` for `PreToolUse`; allowed or
unrelated calls return zero with no output. Malformed envelopes return a denial
without echoing their contents.

From the repository root:

```text
python -X utf8 -m unittest discover -s tests -p test_spawn_contract.py -v
```

An integration check must additionally show both:

- A native spawn with explicit role and `fork_turns: "none"` reaches the child
  and returns its result.
- A native spawn using a history fork is rejected by this hook before the child
  starts. The tool record must show the `Spawn contract:` reason.

Use an isolated disposable project and a dedicated validation conversation.
The negative case deliberately probes the hook's refusal; do not ask an agent to
ignore unrelated authorization or safety controls. A refusal by the model before
calling the tool does not prove hook interception. A TOML parse or the subprocess
unit tests do not prove interception either.

## Coverage and limits

The example matches `spawn_agent`, `Agent`, `agents.spawn_agent`,
`functions.spawn_agent` and `agentsspawn_agent`. The last name was observed in a
real `PreToolUse` event on `codex-cli 0.155.0-alpha.3.10` with V2 namespace `agents`:
the runtime flattens the namespace instead of supplying the traditional spawn
identity. See the [upstream report](https://github.com/openai/codex/issues/36519).
Matching only `spawn_agent` or `Agent` missed that measured native call.

Use the exact hook tool name from the tested runtime, not a substring matcher
that might catch unrelated MCP tools. If you change `tool_namespace`, verify its
emitted identity and adjust both the matcher and guard before relying on this hook.

The [official hooks documentation](https://learn.chatgpt.com/docs/hooks#tool-coverage)
describes `spawn_agent`/`Agent` interception but warns that specialized tool paths
can opt out. See this repository's [validation record](../../docs/validation.md)
for the actual supported baseline and measured outcomes.

Hook discovery, enabled state, trust, interpreter availability and runtime
interception all matter. A disabled, untrusted or failing handler is not an
enforcement boundary. The runtime may continue after a hook infrastructure
failure. Treat warnings and a failed negative check as a broken installation,
not proof that malformed spawns are blocked.

## Remove

Remove only this matcher/handler from hooks.json and its corresponding trust
entry through the normal hook UI. Remove the script when no configuration
references it. Preserve other handlers and do not turn off all hooks. Restart
Codex to verify the configuration.
