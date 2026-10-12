# Windows — experimental, unverified

## Tools for this target

Start with PowerShell metadata, hashes, and signature inspection. Check the
[shared inventory](tools.md) before choosing from this optional catalog. Native
PE code, managed .NET code, and MSIX packaging need different tools.

| Task | Tools and selection notes |
| --- | --- |
| PE headers, symbols, dependencies | [DUMPBIN](https://learn.microsoft.com/en-us/cpp/build/reference/dumpbin-reference) or [LLVM tools](https://llvm.org/docs/CommandGuide/) such as `llvm-readobj` and `llvm-objdump`. Prefer an existing toolchain. |
| Native disassembly and decompilation | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) for PE code. [Binary Ninja](https://binary.ninja/) or [IDA](https://hex-rays.com/ida-pro) are optional alternatives subject to edition/license and architecture support. |
| Scripted native analysis | [PyGhidra](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/PyGhidra/README.md), [Capstone](https://www.capstone-engine.org/), and [LIEF](https://lief.re/) for their respective analysis/format roles. |
| Python PE and .NET inspection | [pefile](https://github.com/erocarrera/pefile) for PE structures, [dnfile](https://github.com/malwarefrank/dnfile) for CLR metadata, [dncil](https://github.com/mandiant/dncil) for CIL decoding. |
| Managed-code analysis and editing | [ILSpy](https://github.com/icsharpcode/ILSpy) for .NET decompilation, [dnSpyEx](https://github.com/dnSpyEx/dnSpy) for supported .NET debugging/assembly editing. Confirm runtime support and preserve assembly identity constraints. |
| Native debugging and crash inspection | [WinDbg](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/). [x64dbg](https://x64dbg.com/) is another choice for x86/x64 user applications, not an ARM64 debugger. |
| File and registry observations | [Process Monitor](https://learn.microsoft.com/en-us/sysinternals/downloads/procmon) with filters for the clone's test process. Ask before any elevation it requires and avoid collecting unrelated user activity. |
| Icons, dialogs, and structured bytes | [Resource Hacker](https://www.angusj.com/resourcehacker/) for supported Win32 resources, [ImHex](https://github.com/WerWolv/ImHex) for inspection. Byte edits invalidate existing signatures. |
| Instruction assembly and isolated tests | [LLVM tools](https://llvm.org/docs/CommandGuide/) or [Keystone](https://www.keystone-engine.org/), plus [Unicorn](https://www.unicorn-engine.org/). Check CPU support and model only the required test context. |
| Small native additions | [MSVC Build Tools](https://learn.microsoft.com/en-us/cpp/overview/acquire-msvc) or an appropriate [LLVM toolchain](https://llvm.org/). Match the target ABI, runtime, and architecture. |
| Signing and packaging | [SignTool](https://learn.microsoft.com/en-us/windows/win32/seccrypto/signtool) and [MakeAppx](https://learn.microsoft.com/en-us/windows/msix/package/create-app-package-with-makeappx-tool) from needed Windows SDK components. Packaging does not grant trust. |

Use [isolated Python environments](tools.md#python-packages). Do not request the
entire Visual Studio or Windows SDK installation for a metadata-only change.
Portable tools and vendor SDKs follow their respective storage/inventory rules.

## Locate and classify

Accept a Start menu name, shortcut, or Explorer selection. Resolve its target
read-only; distinguish a portable/classic Win32 app from MSI-managed software,
MSIX/AppX, Store-protected content, and a service/driver. Record architecture,
dependencies, original Authenticode/package signature, and application identity.

Prefer an authorized portable or unpackaged user app. Do not assume copying one
`.exe` is sufficient. Copy the whole required app directory to the baseline and
working copy, preserving resources and relative layout. Never edit Program Files,
WindowsApps, the original installer's maintenance database, or system binaries.
Do not take ownership of WindowsApps to get around access restrictions.

## Minimal change and independent identity

Check existing PowerShell, SDK, inspection, and compiler tools. Download only
needed components into the documented managed location or index the vendor SDK
location. Resource changes, supported extensions, and small native additions are
preferred to rebuilding the product; binary edits must validate the exact input.

Use a distinct name/icon, install path, and identity where supported. Check
registry keys, AppData, COM registration, protocol handlers, named IPC objects,
services, and auto-updaters; a renamed executable does not isolate them. Do not
share the original's writable databases or service registration silently. Stop
if an independent clone requires protected system changes or cannot be isolated.

## Signing is format-dependent

Changing signed executable bytes invalidates the publisher's signature. Do not
claim the original publisher still vouches for the clone. A project-owned local
test certificate may sign suitable user-mode code; protect its private key and
obtain consent for any certificate installation/trust change. Do not disable
Defender, SmartScreen, WDAC, or driver-signing enforcement to run the result.

MSIX/AppX additionally needs consistent package identity, publisher/certificate,
dependencies, and a supported package-signing/install route. Do not reuse the
original package identity to replace it. Use
[Microsoft's package signing guidance](https://learn.microsoft.com/en-us/windows/msix/package/sign-app-package-using-signtool)
and [local test-certificate guidance](https://learn.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing).
If policy blocks local signing or deployment, report that blocker. Ordinary
portable Win32 apps and MSIX packages do not have identical signing requirements.

## Visible installation and handoff

For a portable clone, prefer `%LOCALAPPDATA%\Programs\<New Name>` and a distinctly
named shortcut in the current user's Start menu Programs folder. Confirm exact
targets before replacing a previous clone and keep a verified rollback archive.
Use the supported per-user package installer for an approved MSIX clone instead
of copying files into protected package directories. Ask before elevation or
system-wide installation; never change default file handlers automatically.

Launch from the actual shortcut/package entry, test the requested behavior and
normal saves with disposable files, and verify the original is unchanged. Tell
the user where to click and how to remove only the clone. Local test signatures
do not confer public trust or software redistribution rights.
