# Linux — experimental, unverified

## Tools for this target

Prefer installed `file` and [GNU Binutils](https://www.gnu.org/software/binutils/)
(`readelf`, `objdump`, `strings`). Use the existing compiler, GDB/LLDB, and
format-specific packaging utilities only when needed. Ghidra is an optional
decompiler, not a prerequisite; do not download Android or Apple SDKs for a
Linux desktop target.

## Find the artifact and packaging boundary

Accept an app-menu name. Inspect its desktop entry, executable location, package
metadata, architecture, and dependencies read-only. Distinguish a portable ELF
application, AppImage, unpacked app bundle, distro package, Flatpak, and Snap.
Never patch a package manager's installed `/usr` files or protected runtimes.

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

## Integrity and a visible launcher

There is no universal Linux app code-signing equivalent to macOS. Respect the
chosen package/container format's integrity and signing requirements; use the
documented developer packaging route when applicable. A checksum or locally
created signature does not make a modified package trusted by its distributor.
Do not forge vendor signatures or weaken package verification.

For an independent user app, stage the clone under
`${XDG_DATA_HOME:-$HOME/.local/share}/omniform/apps/<new-name>/`. Provide a unique
`.desktop` launcher under `${XDG_DATA_HOME:-$HOME/.local/share}/applications/`,
with the actual executable and icon paths, correct escaping, and a distinct ID.
The `Exec` value is not arbitrary shell syntax; follow the
[Desktop Entry specification](https://specifications.freedesktop.org/desktop-entry/latest-single/)
and [XDG directory rules](https://specifications.freedesktop.org/basedir-spec/latest/).
Use supported per-user package registration instead when the chosen format needs it.

Test from the desktop menu, not just an interactive shell with extra environment
variables. Check the new feature, normal behavior, and unchanged original. Explain
how to remove this clone and its launcher without removing shared runtimes or
the original app. Keep a rollback archive and report the tested distribution,
desktop, and architecture. Local functionality does not grant redistribution rights.
