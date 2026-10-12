# macOS — prototype workflow verified

The MyPreview prototype established this workflow on one macOS/Preview setup.
It does not establish compatibility with every Mac app, OS release, entitlement,
or processor architecture. Recheck the actual target before promising a result.

## Tools for this target

Start with installed `plutil`, `file`, `ditto`, and `codesign`. Check the
[tool inventory and storage rules](tools.md) before adding anything. The catalog
is optional and applies to the working copy, not the system app.

| Task | Tools and selection notes |
| --- | --- |
| Architectures, dependencies, symbols | [Apple developer tools](https://developer.apple.com/xcode/resources/) provide `otool`, `lipo`, `nm`, and related utilities. [LLVM tools](https://llvm.org/docs/CommandGuide/) are alternatives for supported object formats. |
| Native disassembly and decompilation | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) for Mach-O analysis. [Hopper](https://www.hopperapp.com/) is an optional commercial alternative. Confirm architecture coverage. |
| Scripted native analysis | [PyGhidra](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/PyGhidra/README.md) for Ghidra automation, [Capstone](https://www.capstone-engine.org/) for instruction decoding. |
| Python executable inspection | [LIEF](https://lief.re/) for structured Mach-O work, [macholib](https://macholib.readthedocs.io/) for headers and dependencies. Use `plistlib` for simple property lists. |
| Objective-C metadata | [class-dump](https://github.com/nygard/class-dump) when compatible with the artifact. Its metadata output is not recovered source or a general Swift decompiler. |
| Instruction assembly and isolated tests | [LLVM tools](https://llvm.org/docs/CommandGuide/) or [Keystone](https://www.keystone-engine.org/) for supported instructions, [Unicorn](https://www.unicorn-engine.org/) for small CPU test cases. Neither recreates AppKit or macOS. |
| Debugging and profiling | [LLDB](https://lldb.llvm.org/) for the clone's process and crashes. [Xcode Instruments](https://developer.apple.com/xcode/) when profiling is needed. Normal debugging permissions still apply. |
| Resources and byte comparison | Installed `plutil`, `sips`, and `iconutil` for relevant metadata/images/icons. [ImHex](https://github.com/WerWolv/ImHex) for structured byte inspection. Do not assume arbitrary asset catalogs can be rebuilt. |
| Small native additions | [Command Line Tools](https://developer.apple.com/documentation/xcode/installing-the-command-line-tools/) for Clang and available SDKs. Use [Xcode](https://developer.apple.com/xcode/) only when the required SDK or asset tooling needs it. |
| Signing and delivery | Installed `codesign` and Keychain tools using [Apple's signing guide](https://developer.apple.com/library/archive/documentation/Security/Conceptual/CodeSigningGuide/Procedures/Procedures.html). Copy with `ditto`, then test the separately named app in Applications. |

Use local manual pages for installed Apple utilities. Check Python package names
and environment rules in [the shared catalog](tools.md#python-packages). Full
Xcode, a Java runtime, and Ghidra are separate decisions, not startup requirements.

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
