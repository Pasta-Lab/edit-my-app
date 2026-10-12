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

## Shared analysis tools

These are optional choices, not an installation checklist. Each target guide
has a task-specific catalog with direct links. Read only the selected guide,
then choose tools that match the artifact, CPU, host, and concrete question.
Availability of a tool does not verify this skill's workflow on that platform.

| Need | Official choices | Selection notes |
| --- | --- | --- |
| Disassembly and decompilation | [Ghidra](https://github.com/NationalSecurityAgency/ghidra), [official releases](https://github.com/NationalSecurityAgency/ghidra/releases) | Relevant to all five targets. Run on a supported desktop host to inspect Mach-O, PE, or ELF code. Use Android-specific tools for APK resources and DEX when appropriate. |
| Scriptable native inspection | [radare2](https://github.com/radareorg/radare2), [Rizin](https://github.com/rizinorg/rizin) | Alternative command-line toolsets. Pick one if needed. |
| Interactive analysis | [Cutter](https://cutter.re/), [ImHex](https://github.com/WerWolv/ImHex) | Cutter is a Rizin-based GUI. ImHex supports structured byte inspection and comparison. |
| Optional commercial analyzers | [Binary Ninja](https://binary.ninja/), [IDA](https://hex-rays.com/ida-pro), [Hopper](https://www.hopperapp.com/) | Check host, CPU, edition, automation features, and license. Never purchase or upload an app to a cloud edition without permission. |
| Object files, symbols, assembly | [LLVM tools](https://llvm.org/docs/CommandGuide/), [GNU Binutils](https://sourceware.org/binutils/) | Examples include `llvm-readobj`, `llvm-objdump`, `llvm-mc`, `readelf`, and `objdump`. Prefer an existing compatible toolchain. |
| Debugging local copies | [LLDB](https://lldb.llvm.org/), [GDB](https://sourceware.org/gdb/), [WinDbg](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/) | Match the OS and architecture. Use the clone's test process, not an unrelated installed app. |
| Runtime observations | [Frida](https://frida.re/docs/home/) | Optional for an authorized, debuggable development copy when normal debugging is insufficient. No jailbreak, protected-process access, or security-check bypass. |

Ghidra is recommended across targets, not required for every edit. Metadata or
resource work may need only existing utilities. For Ghidra, use an official
release archive rather than a source ZIP and read that release's Java/Python
requirements. Keep Java and Ghidra in the inventory as separate dependencies.
Do not turn analysis-tool availability into a promise that decompiled output
can be rebuilt, signed, or installed as an equivalent app.

## Python packages

Package names below are for discovery, not a bulk `pip install` command. Select
only the entries needed for the artifact. Native-code packages must support the
host Python and CPU as well as the target's instruction set or file format.

| Official project | Python package | Use |
| --- | --- | --- |
| [Capstone](https://www.capstone-engine.org/) | `capstone` | Instruction decoding for supported CPUs across all five targets. Not a decompiler or executable-file parser. |
| [Keystone](https://www.keystone-engine.org/) | `keystone-engine` | Assemble small instruction sequences for an authorized change. Check current CPU coverage and maintenance before choosing it. |
| [Unicorn](https://www.unicorn-engine.org/) | `unicorn` | Isolated instruction/function tests. Does not supply the full target OS, its APIs, or a security sandbox. |
| [LIEF](https://lief.re/) | `lief` | Structured inspection and controlled rewriting of Mach-O, PE, and ELF. Does not replace format validation or platform signing. |
| [PyGhidra](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/PyGhidra/README.md) | `pyghidra` | CPython access to Ghidra analysis. Requires a compatible Ghidra installation and Java runtime. |
| [macholib](https://macholib.readthedocs.io/) | `macholib` | Mach-O header and dependency inspection for macOS/iOS artifacts. |
| [pyelftools](https://github.com/eliben/pyelftools) | `pyelftools` | ELF/DWARF inspection for Linux and Android native libraries. |
| [pefile](https://github.com/erocarrera/pefile) | `pefile` | Windows PE headers, imports, sections, and resources. |
| [dnfile](https://github.com/malwarefrank/dnfile), [dncil](https://github.com/mandiant/dncil) | `dnfile`, `dncil` | .NET metadata parsing and CIL decoding, respectively. Not native-code decompilers. |
| [Androguard](https://github.com/androguard/androguard) | `androguard` | Static APK, DEX, manifest, and resource inspection. |
| [angr](https://github.com/angr/angr) | `angr` | Optional, heavier control-flow and symbolic analysis of bounded local test cases. Not an exploit-generation workflow. |
| [Construct](https://github.com/construct/construct) | `construct` | Declarative parsers/builders for custom binary resource formats. |
| [YARA Python](https://github.com/VirusTotal/yara-python) | `yara-python` | Identify known byte patterns locally. A match alone is not proof that a patch location is safe. |

Use Python's standard library first for simple hashes, structured bytes, and
property lists. If packages are necessary, create an isolated
[virtual environment](https://docs.python.org/3/library/venv.html) at a resolved
`<tools-dir>/python/<environment-name>/` path. Check the inventory for a suitable
existing environment before creating another. Do not use system `pip`, `sudo pip`,
or overrides of an externally managed Python installation. A virtual environment
isolates dependencies, not untrusted code or permissions.

Use that environment's absolute Python path for package management and execution.
Obtain distribution names from the linked official project, verify current host
support, and inspect optional native/runtime dependencies before installing.
Record interpreter path, package versions actually installed, provenance, and
successful import checks in the inventory. Do not upgrade a working environment
for another project or introduce a pinned universal requirements file.

## Platform catalogs

Open only the current target: [macOS](macos.md#tools-for-this-target),
[iOS](ios.md#tools-for-this-target), [Windows](windows.md#tools-for-this-target),
[Linux](linux.md#tools-for-this-target), or [Android](android.md#tools-for-this-target).
Each includes inspection, native analysis, relevant Python packages, debugging,
resources, build/signing, and deployment choices. No tool in these catalogs is
downloaded by the skill installer.

## Coding agents

Prefer the user's existing local coding agent. Examples are
[Codex](https://developers.openai.com/codex/),
[Claude Code](https://code.claude.com/docs/en/overview), and
[Gemini CLI](https://github.com/google-gemini/gemini-cli). This is a portable
instruction workflow, not an endorsement or a compatibility test of every host.
Do not install another agent, start additional paid sessions, or delegate work
unless the user and the current host's instructions allow it. No specific model,
subagent, MCP server, or network service is required.
