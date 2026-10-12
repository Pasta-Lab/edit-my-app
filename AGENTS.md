# Repository Guidelines

## Purpose

This repository distributes Edit My App, a lightweight Omniform Software
Engineering skill. It teaches agents to customize authorized copies of compiled
applications. Maintaining this repository does not itself authorize modifying
or installing any application.

## Structure

`skills/edit-my-app/SKILL.md` is the provider-neutral entry point. Its
`references/` directory contains the shared workflow, optional tool catalog,
and five target-platform guides. `plugin.json` is an optional packaging manifest;
there are no hooks, background services, or bundled analysis tools.

## Conventions

Write concise, actionable Markdown for agents serving nontechnical users.
Load only the relevant target-platform guide; distinguish target OS from host
OS. Keep macOS's prototype verification separate from the unverified platform
guides. Link to official tool pages rather than pinning tool versions. Record
observed tool versions in user projects for reproducibility.

Keep installers dependency-free apart from the host shell and standard file
utilities; remote installation additionally uses HTTPS. Never install SDKs,
agents, or binary tools during skill installation. Keep installer file lists
in sync with the skill package. Never overwrite an existing skill directory.

## Verification

Run `python3 -B tests/check.py` for package and offline installer checks. Python
is a contributor test dependency, not an installation dependency. Run
`bash -n install.sh` after shell edits. PowerShell and non-macOS runtime behavior
must remain labeled unverified until tested on those systems.

Use synthetic fixtures and isolated temporary destinations. Do not test by
changing system apps, trust stores, real agent configuration, or user documents.
Do not publish, push, or install globally without an explicit request.
