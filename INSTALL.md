# Installation

## macOS / Linux: local checkout

For the hosted installer, see [Install](README.md#install). To install from a
downloaded or cloned repository, open Terminal in its folder and run:

```sh
bash ./install.sh
```

If the repository is private, sign in to GitHub to download it or use an
authenticated clone. The README's public `curl` command will not work until
the repository is publicly readable; no visibility changes are made by installers.

The Bash installer has been tested on macOS; Linux installation is unverified.

The default destination is `~/.agents/skills/edit-my-app`, a
[Codex user skill location](https://learn.chatgpt.com/docs/build-skills).
The installer writes only this skill's text files. It never changes your app,
shell profile, tool installations, or agent settings. Existing destinations are
left untouched. Start a new agent conversation; restart the agent if necessary.

## Other agents

For [Claude Code](https://code.claude.com/docs/en/skills):

```sh
bash ./install.sh --agent claude
```

This uses `~/.claude/skills/edit-my-app`. For another Agent Skills-compatible
host, point `--dest` at its documented **skills parent directory**:

```sh
bash ./install.sh --dest /absolute/path/to/skills
```

Alternatively ask your existing agent: “Install the skill from
`https://github.com/Pasta-Lab/edit-my-app/tree/main/skills/edit-my-app`.” It should
inspect the files first. No particular agent or paid model is required by this
package; your chosen agent may have its own requirements and charges.

If a host only supports `AGENTS.md`, ask it to read
`skills/edit-my-app/SKILL.md` for this task, or add a reference to that file in an
existing project guide. Do not replace unrelated project or global instructions.

## Windows — unverified

[Download the ZIP](https://github.com/Pasta-Lab/edit-my-app/archive/refs/heads/main.zip)
and extract it, or clone the repository. Open PowerShell in that repository
folder and run:

```powershell
.\install.ps1
```

`-Agent claude` and `-Destination 'C:\absolute\skills'` select other hosts. If
organizational policy blocks scripts, ask your agent to copy the skill directory
instead; do not weaken execution policy. This PowerShell installer needs the
complete downloaded repository; it does not support piping a remote script.

## iOS / Android targets

Install the skill on the computer running your coding agent, using the host's
instructions above. The agent loads the iOS or Android guide as needed; there
is no phone-side skill installer. Both mobile workflows are unverified.

## What gets installed?

Only `SKILL.md`, its reference Markdown files, and the MIT license. The five
small platform guides are present on disk, but the router loads just the selected
target's guide. Downloads of optional tools happen later, separately, under
[the documented tool directory](skills/edit-my-app/references/tools.md).

`plugin.json` also allows skills-only plugin packaging in compatible hosts;
plugin-store publication and cross-host plugin installation have not been tested.
No MCP server, lifecycle hook, or automatic background action is included.

## Update or remove

An installer rerun never overwrites your existing skill. To update, first move
the exact `edit-my-app` skill folder somewhere **outside** your agent's scanned
skill directories as a backup, then reinstall. For removal, move that same folder
to Trash. Do not delete the entire skills directory. Apps, project backups, and
downloaded tools are independent and are not removed by uninstalling this skill.
