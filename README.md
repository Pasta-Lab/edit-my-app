# Edit My App

**Omniform Software Engineering:** describe a change, and your AI coding agent
adapts an existing compiled app instead of rebuilding the whole product.

For example: “Add an AI sidebar to Preview, but keep my original app untouched.”
The agent finds the app, works on a copy, tests it, and helps you open the result.

## Install

Install on **the computer running your agent**, not the app's target device.
These commands use Codex's skill directory.
See [other agents and custom locations](INSTALL.md) for alternatives.

### macOS / Linux

Paste into Terminal (Linux installation is unverified):

```sh
curl -fsSL https://raw.githubusercontent.com/Pasta-Lab/edit-my-app/main/install.sh | bash
```

This link requires a public repository. While private, use an authenticated
download or clone and follow [local installation](INSTALL.md#macos--linux-local-checkout).

### Windows (unverified)

[Download the ZIP](https://github.com/Pasta-Lab/edit-my-app/archive/refs/heads/main.zip),
extract it, open PowerShell in the extracted repository folder, and run:

```powershell
.\install.ps1
```

iOS and Android use a desktop agent, not an installer running on the phone.

Then tell your agent: **“Use edit-my-app to change [app name] so it [does this].”**
You need a local coding agent with file and terminal access. Review the
[Bash](install.sh) or [PowerShell](install.ps1) installer before running it.

The installer adds instructions only. Agents choose from the optional
[tool catalog](skills/edit-my-app/references/tools.md), check existing tools,
and download only what they need. Only the relevant platform guide is loaded.

## Permissions

Your agent may need broader file, terminal, or network access. Some steps also
need administrator approval, signing permissions, or device access. The agent
should explain each request. Grant only what that step needs and keep system
protections enabled.

## What is supported?

**Only macOS has been verified so far.**

| App platform | Status |
| --- | --- |
| [macOS](skills/edit-my-app/references/macos.md) | Verified |
| [iOS / iPadOS](skills/edit-my-app/references/ios.md) | Unverified |
| [Windows](skills/edit-my-app/references/windows.md) | Unverified |
| [Linux](skills/edit-my-app/references/linux.md) | Unverified |
| [Android](skills/edit-my-app/references/android.md) | Unverified |

Not every app is modifiable. Some require source access or developer provisioning.

Original apps stay untouched. On macOS, successful builds receive a distinct
name and local signature and are installed in Applications with your approval.

Generated apps are **personal experiments, not ready for distribution**.
Personal use and local signing do not grant modification or distribution rights.
The skill is [MIT licensed](LICENSE). That license does not cover other apps or tools.
