# Windows sandbox startup and temporary directories

Keep the sandbox enabled when testing an arrangement. A model that replies, or
a command that runs outside the sandbox, does not prove sandboxed tool execution.

## Measured startup failure

On Windows with Codex `0.155.0-alpha.3.10`, the isolated validation runner inherited
the host's shared `TEMP` and `TMP`. Even a sandboxed `cmd.exe /d /c echo` exceeded
20- and 40-second deadlines. The process was active: a six-second observation
recorded about 136,000 additional non-read/write I/O operations, with unchanged
ordinary read and write counts. This is consistent with metadata preparation,
but the counters alone do not identify the paths or operations.

Changing only the child process's `TEMP` and `TMP` to an owned empty directory
made the identical command return the expected output with exit code 0. Its
native sandbox log recorded 66 ms between `START` and `SUCCESS`. The workspace
permission profile, Windows sandbox backend and private desktop were unchanged.
This identifies a temporary-directory-dependent startup problem; it does not
prove which internal enumeration or ACL operation was responsible.

## Separate Store PowerShell limitation

After that correction, the Store/MSIX build of PowerShell 7.6.6 still failed
before execution with `CreateProcessAsUserW failed: -1073283067`; its App Execution
Alias failed with error 5. In the same sandbox, `cmd.exe` succeeded. These outcomes
were unchanged with or without the test's Windows Job Object.

A Microsoft-signed official ZIP of the same PowerShell version succeeded in one
diagnostic comparison. That was a packaging contrast, not an installation change
or a substitute for testing the Store shell. The existing Store installation and
global PATH were preserved. The independent native artifact review remains unverified.
An earlier [upstream user report](https://github.com/openai/codex/issues/35871)
describes a similar failure; it is not a maintainer-confirmed resolution.

## Isolate test runners

For an isolated Codex test process:

1. Create a new, unique temporary directory inside the test's owned area.
2. Set both `TEMP` and `TMP` in the environment passed to Codex itself, before
   sandbox initialization. Setting them only in the eventual shell is too late.
3. Keep the directory alive until that root and all its children have exited.
4. Apply a bounded deadline and terminate only the process tree the test started.
5. Remove only the owned temporary directory after execution ends.

Do not change user- or machine-wide environment variables, purge the host's Temp
directory, kill unrelated console processes, or disable sandbox controls. A test
that needs a preexisting temporary artifact must receive that input explicitly;
it should not depend on the host's shared temporary files.

This is a test-runner isolation measure, not an extra arrangement TOML setting.
Use the [runtime evidence](runtime-evidence.json) to distinguish this command
check from the separate native agent, artifact and capacity scenarios.

The [official Windows sandbox guide](https://learn.chatgpt.com/docs/windows/windows-sandbox)
explains supported backends and diagnostic logs. The exact tested CLI tag resolves
to [this source commit](https://github.com/openai/codex/tree/f5e8906cd6ccfdd6e6f61c8ce44ea6b1ef1912c0).
Microsoft documents the [distinct PowerShell installation packages](https://learn.microsoft.com/en-us/powershell/scripting/install/install-powershell-on-windows?view=powershell-7.6);
the diagnostic ZIP came from the [official 7.6.6 release](https://github.com/PowerShell/PowerShell/releases/tag/v7.6.6).
