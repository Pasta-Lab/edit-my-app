# Edit My App

**Omniform Software Engineering:** describe a change, and your AI coding agent
adapts an existing compiled app instead of rebuilding the whole product.

For example: “Add an AI sidebar to Preview, but keep my original app untouched.”
The agent finds the app, checks feasibility, works on a copy, tests it, and helps
you open the result like a normal app. You do not need to know binary formats.

## Install

Choose the installer for **the computer running your agent**, not the app you
want to modify. These commands install the skill for Codex;
[other agents and custom locations](INSTALL.md) are supported.

### macOS / Linux

Paste into Terminal (Linux installation is unverified):

```sh
curl -fsSL https://raw.githubusercontent.com/Pasta-Lab/edit-my-app/main/install.sh | bash
```

### Windows — unverified

[Download the ZIP](https://github.com/Pasta-Lab/edit-my-app/archive/refs/heads/main.zip),
extract it, open PowerShell in the extracted repository folder, and run:

```powershell
.\install.ps1
```

iOS and Android use a desktop agent, not an installer running on the phone.

Then tell your agent: **“Use edit-my-app to change [app name] so it [does this].”**
You need a local coding agent with file and terminal access. Review the
[Bash](install.sh) or [PowerShell](install.ps1) installer before running it.

The installer adds instructions only—no binary tools, SDKs, agents, or services.
Tools are optional, chosen by your agent, and downloaded only when
needed. Existing installations are checked first. Only the relevant platform
guide is loaded into the agent's context.

## What is supported?

**Only macOS has been verified so far.**

| App platform | Status |
| --- | --- |
| macOS | Verified with the MyPreview prototype |
| iOS / iPadOS | Experimental; unverified |
| Windows | Experimental; unverified |
| Linux | Experimental; unverified |
| Android | Experimental; unverified |

Not every app is modifiable; some require source access or developer provisioning.

Original apps stay untouched. On macOS, successful builds receive a distinct
name and local signature and are installed in Applications with your approval.

Generated apps are **personal-use experiments, not distribution-ready**.
Licenses may restrict modification or sharing; local signatures and provisioning
do not provide public distribution approval. Personal use is not automatically
legal. The skill itself is [MIT-licensed](LICENSE); third-party apps and tools
are not covered by that license.
