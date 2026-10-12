# Windows — experimental, unverified

## Tools for this target

Start with PowerShell metadata/hash/signature inspection. Add only needed
[Windows SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/)
components such as SignTool or MakeAppx. Use
[WinDbg](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/)
for local debugging, [ILSpy](https://github.com/icsharpcode/ILSpy) for a .NET
target, or a shared native analyzer for PE code when warranted. Native additions
may need matching compiler build tools; resource inspection does not always do so.

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
