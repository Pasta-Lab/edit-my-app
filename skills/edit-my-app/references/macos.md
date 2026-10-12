# macOS — prototype workflow verified

The MyPreview prototype established this workflow on one macOS/Preview setup.
It does not establish compatibility with every Mac app, OS release, entitlement,
or processor architecture. Recheck the actual target before promising a result.

## Tools for this target

Start with installed `plutil`, `file`, `ditto`, `codesign`, and the selected
[Apple developer tools](https://developer.apple.com/xcode/resources/): `otool`,
`lipo`, `clang`, and LLDB as needed. Resource-only work may need no compiler;
full Xcode and Ghidra are not automatic prerequisites. Check the shared tool
inventory and host-specific storage contract before downloading anything.

## Find the app and check prerequisites

An app name is enough to start. Inspect Applications, the user's Applications
folder, and the corresponding system app location; use Spotlight metadata or a
Finder selection if necessary. Show the user the matching app names/locations
when several exist. Confirm the exact `.app` bundle, not just an executable or
the internal `Contents` directory. Do not ask a nontechnical user for Mach-O paths.

Read the bundle metadata, executable architectures, dependencies, signature, and
entitlements. Check `xcode-select -p` and `xcrun --find clang`. If compilation is
needed and tools are missing, explain Apple's installation dialog before
requesting the [command-line tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools/).
Use full Xcode only when its SDKs/features are actually needed. Let the user
accept licenses, installation prompts, and required permissions; do not silently
change the active developer directory or enable broad developer privileges.

## Clone and change only the copy

Copy the complete app bundle to the project's untouched baseline, then derive
a working copy. Preserve framework symlinks, modes, resources, and metadata;
`ditto` is available for bundle copying. Never edit `/System/Applications` or
the original app under `/Applications`, and never re-sign either one.

Use a distinct display name, bundle identifier, and recognizable icon. Inventory
nested helpers and services; changing the top-level identifier alone is not data
isolation. Check shared containers, preferences, file associations, URL handlers,
cloud services, login helpers, and update behavior. Keep an updater from replacing
the original through the clone; if that cannot be safely isolated, stop.

Reuse the existing UI and document workflows. Prefer narrow resource changes,
supported extension points, or a small native addition. Any binary change must
be specific to a verified input and architecture. Do not reuse offsets from
another app/version, claim a launcher script modifies the binary, or rewrite the
whole app. Preserve the baseline for rebuilding after each experiment.

## Local signing and launch

Use a dedicated project-owned local **code-signing** identity with its private
key in Keychain. Explain any necessary trust prompt and keep trust scoped to
code signing, not a new general-purpose trusted root. Do not change trust stores
without consent, use the original publisher's identity, or copy restricted
Apple-only entitlements into locally signed code. Some protected features simply
will not work; report them rather than disabling platform protections.

Finish modifications first. Sign modified nested code inside-out, then the outer
bundle; verify with `codesign --verify --strict --verbose=2` and inspect nested
components. Signature validity is not the same as Gatekeeper acceptance or
notarization. Test an actual launch without disabling SIP, AMFI, Gatekeeper, or
system-wide library validation. Use normal, app-specific approval UI only when
appropriate and explain it to the user. See [Apple's signing guide](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/Procedures/Procedures.html).

## Deliver an app the user can find

After tests, ask the user to save and quit the clone. With the normal filesystem
authorization, stage the uniquely named result as `/Applications/<New Name>.app`.
If that needs unavailable administrator permission, offer `~/Applications`
explicitly instead. Never overwrite the original or an unrelated same-name app.
Back up and verify any earlier modified version before replacing it.

Recheck the installed signature, launch the installed copy, verify the feature
there, and reveal it in Finder. Tell the user its name, where to click, how to
add it to the Dock if desired, and how to remove only this copy. Do not make it
the default document handler automatically. Keep prior builds in ZIP backups
so they do not crowd Open With; never launch/register the baseline as a new app.

State that generated apps are not for redistribution: the original
[software license](https://www.apple.com/legal/sla/) may restrict modification
and redistribution, and a local development signature is not a distribution
identity or notarization. The skill's MIT license does not cover copied apps.
