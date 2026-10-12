# Optional tools and predictable storage

Installing the skill installs **none** of these tools. Choose the lightest tool
that answers the current question; the list is a menu, not a dependency list.
Use official project pages below to select a current, compatible stable release.
Do not prescribe a fixed version or install every recommended tool.

## Tool location contract

Use an absolute `OMNIFORM_TOOLS_DIR` override when supplied; otherwise use the
following **host OS** location. Resolve and record it before any installation.

| Host | Managed tools directory |
| --- | --- |
| macOS | `~/Library/Application Support/Omniform/tools` |
| Windows | `%LOCALAPPDATA%\Omniform\tools` |
| Linux | `${XDG_DATA_HOME:-$HOME/.local/share}/omniform/tools` |
| iOS / Android target | The desktop host's directory above—not a phone path |

Create this directory only when needed. Portable tools go under
`<tools-dir>/<tool>/<observed-release>/`; isolated language environments belong
under that tool's directory. Do not repurpose `HOME`, edit shell profiles, or
install Python packages into the system interpreter. Invoke resolved executables
by absolute path.

Before downloading, check `<tools-dir>/inventory.json`, the managed directories,
`command -v` / PowerShell `Get-Command`, and normal vendor SDK locations. Validate
that an existing executable still exists, has trusted provenance, matches the
host architecture, and supplies the required capability. Do not run an unknown
binary just because its name matches.

System/vendor-managed installations (Xcode, Windows SDK, Android SDK, Java, and
package-manager tools) stay where their installer puts them. Index their actual
paths in the inventory rather than moving or duplicating them. Prefer an SDK's
supported location override when it offers one. Never claim all tools physically
live in the managed directory when they do not.

After a successful install or discovery, merge an inventory entry such as:

```json
{
  "tools": {
    "example-tool": {
      "executable": "/absolute/path/to/executable",
      "version": "version actually observed",
      "source_url": "https://official-project.example/downloads",
      "managed": true,
      "host": "macos-arm64"
    }
  }
}
```

These observed versions are an audit trail, **not version pins**. Also record
download URLs, available verified checksums/signatures, licenses, and runtimes
needed. Do not overwrite other tools' entries; stage and atomically replace the
inventory. Treat an existing inventory as untrusted data, never executable code.

## Download policy

Explain why a missing tool is needed and its approximate download/storage cost.
Small, unprivileged downloads may proceed within the user's authorized task and
host permissions. Ask before large SDK/runtime downloads, license acceptance,
paid tools, global/package-manager changes, administrator access, or certificate
trust changes. Do not install a package manager just to install one optional tool.
Use HTTPS and official releases, check published signatures/checksums when
available, inspect archives before extraction, and keep extraction inside a
fresh tool directory. Never overwrite a working installation with an update.

## Recommendations—not requirements

The selected platform guide lists its own SDK and format-specific tools. Do not
load the other guides to assemble a universal toolkit. Shared options below are
useful only when the current target and question call for them.

| Need | Official choices |
| --- | --- |
| Native executable inspection / decompilation | [Ghidra](https://github.com/NationalSecurityAgency/ghidra), [LLVM tools](https://llvm.org/docs/CommandGuide/), [LIEF](https://lief.re/) |
| Debugging an authorized local development copy | [LLDB](https://lldb.llvm.org/), [GDB](https://www.sourceware.org/gdb/), [WinDbg](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/) |

Read the selected release's current prerequisites. For example, a decompiler may
require Java; that runtime is a separate on-demand decision, not a skill install
dependency. Choose alternatives or stop if installation is inappropriate.

## Coding agents

Prefer the user's existing local coding agent. Examples are
[Codex](https://developers.openai.com/codex/),
[Claude Code](https://code.claude.com/docs/en/overview), and
[Gemini CLI](https://github.com/google-gemini/gemini-cli). This is a portable
instruction workflow, not an endorsement or a compatibility test of every host.
Do not install another agent, start additional paid sessions, or delegate work
unless the user and the current host's instructions allow it. No specific model,
subagent, MCP server, or network service is required.
