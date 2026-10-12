# Common workflow

## 1. Establish the target and a feasible first change

Record the resolved app path/package, displayed name, version, target OS,
architectures, signature/provisioning status, and user's requested behavior.
Inspect metadata and existing extension/resource mechanisms before installing
tools. Confirm the user has permission to work on this app. Exclude kernel
components, security agents, DRM/license checks, and other protected components.
An installed app is not necessarily a freely copyable or modifiable app.

Offer the smallest useful change first. Prefer supported extension points or
packaged resources when they satisfy the request; a bounded binary change or a
small native addition can be appropriate for an authorized copy. Do not replace
the original application with a newly written imitation. Explain when the chosen
solution is a companion/automation script instead of an in-app modification.

## 2. Preserve the original and isolate its data

Choose a dedicated project folder with the user, defaulting to an app-specific
folder under `~/Omniform/` (the user's profile directory on Windows). Resolve
symlinks and ensure source, baseline, working copy, and installation destination
are distinct. Copy the complete required app/package and resources, preserving
metadata and internal symlinks without traversing links into external locations.
Never use a hard link as a mutable copy. Record content hashes and link targets.

Keep an untouched baseline, a separate working copy, patch/build scripts, test
fixtures, and a short change log. Do not register or launch the baseline. Keep
old builds as verified archives outside app-launcher discovery locations.

A new app name or identifier does **not** guarantee data isolation. Check shared
preferences, app groups, credential stores, absolute data paths, databases,
helpers, cloud sync, and updaters. Use disposable documents and a separate profile
where possible. If safe isolation is uncertain, explain that before any launch.
Do not move/delete original app data or silently enable its updater in the clone.

## 3. Make bounded, repeatable changes

Create a repeatable script for the exact identified input—not a universal patch
for unknown versions. Before each write, verify the expected file hash/version,
architecture, and original bytes or structure. Refuse unknown inputs, repeated
application, or ambiguous matches. Record every changed file and the reason.
Keep replacement assets and any added code separate from the intact baseline.

Preserve unrelated code, resources, accessibility, localization, and document
behavior. Respect instruction alignment, object lifetime, calling conventions,
and platform format constraints. Do not remove security checks to make a patch
fit. If the change needs a substantially different architecture or permissions,
stop and explain the tradeoff rather than growing the task silently.

Changes must be reversible; generated output must never overwrite user files.
When adding AI functionality, use explicit user-triggered requests, cancellation,
visible progress, bounded operations, and OS-backed secret storage. Start with
mock responses; live requests and charges require permission.

## 4. Validate, sign where applicable, then test

Verify structure and dependencies before execution. Follow only the relevant
platform's signing/provisioning rules; no universal signing recipe applies.
Sign the final clone, not the original. Keep private keys out of source control,
logs, command-line arguments, app bundles, and shared archives.

Test startup, the new behavior, existing core features, saves/reopens, errors,
Undo/cancellation where applicable, and quitting/relaunching. Use disposable data
and offline fixtures; screenshots alone do not prove persistence or correctness.
Inspect crashes before trying another change. Recheck original hashes afterwards
and investigate unexpected differences rather than restoring over user updates.

## 5. Install and hand off

Ask the user to save and quit the **modified copy** before updating it. Confirm
the exact destination and distinct identity; never replace the original app.
For an existing clone, create and verify a recoverable backup before staging an
update. Verify the installed artifact and launch it by the user's normal UI
entry point. Never broaden privileges or alter default handlers automatically.

Report what was actually tested on this OS/version, where to click, remaining
limitations, data/network behavior, and simple rollback/removal instructions.
Do not distribute generated third-party app copies through this workflow.
Licenses and local signing both matter; consult the target's license, not an
assumption that personal use is always allowed.
