# Linux — experimental, unverified

## Tools for this target

Prefer installed `file`, `readelf`, `objdump`, and `strings`. Check the
[shared inventory](tools.md) before adding a tool. Match both distribution/host
support and the target's ABI. Do not install mobile or Apple SDKs for this target.

| Task | Tools and selection notes |
| --- | --- |
| ELF metadata, symbols, debug information | [GNU Binutils](https://sourceware.org/binutils/), [elfutils](https://sourceware.org/elfutils/), or [LLVM tools](https://llvm.org/docs/CommandGuide/). Static inspection avoids executing an unfamiliar binary just to list dependencies. |
| Native disassembly and decompilation | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) for ELF code. [Rizin](https://github.com/rizinorg/rizin), [Cutter](https://cutter.re/), or [radare2](https://github.com/radareorg/radare2) are alternative analysis interfaces. |
| Python ELF and instruction inspection | [pyelftools](https://github.com/eliben/pyelftools) for ELF/DWARF, [LIEF](https://lief.re/) for structured ELF work, [Capstone](https://www.capstone-engine.org/) for instructions. |
| Scripted decompilation and deeper analysis | [PyGhidra](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/PyGhidra/README.md). [angr](https://github.com/angr/angr) is an optional heavier choice for bounded local control-flow/symbolic tests. |
| Debugging and runtime diagnosis | [GDB](https://sourceware.org/gdb/) or [LLDB](https://lldb.llvm.org/). [strace](https://strace.io/) for the clone's system calls, [Valgrind](https://valgrind.org/) for supported memory/runtime checks. Respect process-access policy. |
| Local dependency/layout adjustments | [patchelf](https://github.com/NixOS/patchelf) for supported ELF metadata changes. Never use it to redirect system-wide loading or modify the original app. |
| Instruction assembly and isolated tests | [LLVM tools](https://llvm.org/docs/CommandGuide/) or [Keystone](https://www.keystone-engine.org/), plus [Unicorn](https://www.unicorn-engine.org/). CPU emulation does not reproduce a full Linux process environment. |
| Resources and binary comparison | [ImHex](https://github.com/WerWolv/ImHex) or existing byte-comparison utilities. Use [Construct](https://github.com/construct/construct) only if a custom binary resource needs a parser. |
| Small native additions | Existing [GCC](https://gcc.gnu.org/) or [Clang](https://clang.llvm.org/) with matching development headers. Do not replace the distribution's toolchain or shared runtime. |
| Packaging when applicable | [appimagetool](https://github.com/AppImage/appimagetool), [Flatpak Builder](https://docs.flatpak.org/en/latest/flatpak-builder.html), or [Snapcraft](https://documentation.ubuntu.com/snapcraft/stable/). Select only the input's supported packaging route. |
| Visible desktop launcher | Follow the [Desktop Entry specification](https://specifications.freedesktop.org/desktop-entry/latest-single/) and [desktop-file-utils](https://wiki.freedesktop.org/www/Software/desktop-file-utils/) validation where available. |

Use [isolated Python environments](tools.md#python-packages). Tools requiring a
new system package, a container service, or elevated process access need a
separate permission decision. Ghidra is optional, not a launch prerequisite.

## Find the artifact and packaging boundary

Accept an app-menu name or CLI command. Inspect its desktop entry when present,
executable location, package metadata, architecture, and dependencies read-only.
For a CLI app, record the resolved command and executable path. Distinguish a
portable ELF application, AppImage, unpacked app bundle, distro package, Flatpak,
and Snap. Never patch a package manager's installed `/usr` files or protected
runtimes.

Work on a full, authorized copy in the user's project. Package-managed apps may
need a supported export or separately staged package; copying an ELF executable
alone may omit required resources. Do not install over the original package or
modify a shared Flatpak/Snap runtime. If the format has no safe independent-copy
route, explain the limitation and ask about an authorized portable alternative.

## Inspect and adapt without changing the system

Check existing `file`, `readelf`, `objdump`, and compiler/debugger tools first.
Use static dependency inspection such as `readelf -d` for unfamiliar binaries;
do not run `ldd` on untrusted executables. Add Ghidra or another optional tool
only when a concrete question requires it.

Preserve architecture, interpreter/loader, ABI, library dependencies, resources,
and file modes. Use narrow resource changes, supported extensions, or small
additions; bounded binary changes must reject unexpected input hashes. Do not
copy setuid/setgid bits or capabilities into a clone and execute them; stop for
a user-mode alternative when elevated capabilities are essential.

Check shared XDG configuration/state directories, D-Bus names, IPC endpoints,
desktop IDs, update services, and hard-coded original paths. Set up separate
clone configuration through supported mechanisms; do not redirect system-wide
library searches or disable SELinux/AppArmor. Never change global loader settings
to make a local patch work.

## Integrity and launch route

There is no universal Linux app code-signing equivalent to macOS. Respect the
chosen package/container format's integrity and signing requirements; use the
documented developer packaging route when applicable. A checksum or locally
created signature does not make a modified package trusted by its distributor.
Do not forge vendor signatures or weaken package verification.

For an independent user app, stage the clone under
`${XDG_DATA_HOME:-$HOME/.local/share}/omniform/apps/<new-name>/`. For a desktop
app, provide a unique `.desktop` launcher under
`${XDG_DATA_HOME:-$HOME/.local/share}/applications/`, with the actual executable
and icon paths, correct escaping, and a distinct ID. The `Exec` value is not
arbitrary shell syntax; follow the
[Desktop Entry specification](https://specifications.freedesktop.org/desktop-entry/latest-single/)
and [XDG directory rules](https://specifications.freedesktop.org/basedir-spec/latest/).
Use supported per-user package registration instead when the chosen format needs it.

For a CLI app, use a terminal command as the launch route. A desktop launcher is optional. In WSL or other headless environments, test from a terminal and report that desktop menu launch is not applicable. Use an app supported profile override or isolated XDG directories for test data. For a protocol change, use a disposable local fixture bound to loopback and capture the exchanged commands. Do not validate behavior changing patches on public services.

For desktop apps, test from the desktop menu, not just an interactive shell with
extra environment variables. Check the new feature, normal behavior, and unchanged
original. Explain how to remove this clone and its launcher without removing
shared runtimes or the original app. Keep a rollback archive and report the tested
distribution, desktop or terminal route, and architecture. Local functionality
does not grant redistribution rights.
