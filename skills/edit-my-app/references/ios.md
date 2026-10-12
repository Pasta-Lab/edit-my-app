# iOS / iPadOS — experimental, unverified

## Tools for this target

Run analysis tools on the desktop host. For the supported development route,
use a compatible Mac/Xcode setup. Mac command-line tools alone are not an iOS
SDK. Check [the inventory](tools.md) before downloads. This catalog does not
make an encrypted or unprovisioned app a usable input.

| Task | Tools and selection notes |
| --- | --- |
| Bundle and architecture inspection | [Apple developer tools](https://developer.apple.com/xcode/resources/) including `otool`, `lipo`, `nm`, and installed `plutil`. Inspect the supplied developer or simulator artifact. |
| Native disassembly and decompilation | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) on the desktop host for authorized, unencrypted Mach-O code. [Hopper](https://www.hopperapp.com/) is an optional commercial alternative. |
| Scripted native analysis | [PyGhidra](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/PyGhidra/README.md) for Ghidra automation and [Capstone](https://www.capstone-engine.org/) for supported CPU instructions. |
| Python package inspection | [LIEF](https://lief.re/) and [macholib](https://macholib.readthedocs.io/) for Mach-O structures. Standard `plistlib` can read property lists. None decrypts protected apps or supplies provisioning. |
| Language metadata | [class-dump](https://github.com/nygard/class-dump) for compatible Objective-C metadata. Use the matching [Swift toolchain](https://www.swift.org/tools/) for Swift symbol demangling, not source reconstruction. |
| Instruction assembly and unit tests | [LLVM tools](https://llvm.org/docs/CommandGuide/) or [Keystone](https://www.keystone-engine.org/), plus [Unicorn](https://www.unicorn-engine.org/) for bounded CPU tests. A CPU emulator is not an iOS runtime. |
| Debugging and profiling | [LLDB](https://lldb.llvm.org/) and [Xcode Instruments](https://developer.apple.com/xcode/) for permitted developer builds. Device pairing and debugging entitlements still apply. |
| Resources and native additions | [Xcode](https://developer.apple.com/xcode/) for iOS SDKs, asset tools, Clang/Swift, and Interface Builder where usable resources exist. [ImHex](https://github.com/WerWolv/ImHex) for byte inspection. |
| Signing, simulator, and device delivery | [Xcode developer tools](https://developer.apple.com/documentation/xcode) including the available `simctl` and `devicectl`. Follow valid Apple development provisioning, not desktop self-signing. |
| Optional paired-device information | [libimobiledevice](https://libimobiledevice.org/) for supported device communication when needed. Pairing requires user consent. It is not a replacement for Apple signing or a route to private app data. |

Keep tools in the desktop host's managed directory or index their existing SDK
paths. Follow [Python environment rules](tools.md#python-packages). Do not
install a phone-side analysis service or exploitation toolkit as a prerequisite.

## Feasibility comes first

Ask which app, which iPhone/iPad, and whether the user has an authorized developer
build or simulator build. Find a supplied `.ipa` or `.app` on the desktop host
when possible; do not expect a phone user to know filesystem paths.

Unlike macOS, an arbitrary installed App Store app cannot generally be copied,
modified, and installed with an ordinary self-signed certificate. Device code
signing and provisioning are enforced. Require a lawful, unencrypted development
artifact, valid development signing/provisioning, and entitlements allowed for
that identity. If those are absent, stop the binary-editing path and offer a
supported Shortcut, extension, or a developer-provided build. Do not dump or
decrypt protected apps, jailbreak a device, or bypass platform validation.
See [Apple's iOS signing model](https://support.apple.com/guide/security/app-code-signing-process-sec7c917bf14/web).

## Host, copy, and build

A physical-device development workflow normally requires a compatible Mac/Xcode
setup. Check existing tools before requesting the large Xcode download. A
simulator binary is not a device binary; record the platform, architecture, app
identifier, signing team, provisioning expiration, and target device.

Work from an untouched copy of the complete authorized package. Give the clone
its own identifier and name, and account for extensions, app groups, keychain
groups, push notifications, associated domains, and embedded frameworks. Do not
reuse original identifiers to overwrite the installed app. If a separate clone
cannot run correctly with the available entitlements, say so before proceeding.
Make only a bounded resource/binary/native-addition change to the working copy.

## Install with supported development tooling

Use the user's own Apple development identity and a valid provisioning profile,
not the macOS self-signed recipe. The user must handle Apple account login,
device pairing, and any trust prompts. Explain
[Developer Mode](https://developer.apple.com/documentation/xcode/enabling-developer-mode-on-a-device/)
only if the chosen supported development route needs it; never toggle settings
or accept security prompts on the user's behalf.

Sign compatible nested components and the app using the provisioned identity.
Validate identifiers, entitlements, device eligibility, and expiration before
installation. Use current supported Xcode/device tooling and test a separate
app on the authorized device or simulator. A simulator test is not a physical
device validation. Never uninstall the original to resolve a signing conflict.

Confirm the distinct icon appears on the device's Home Screen/App Library, test
launch and the requested feature, and explain how to remove the clone. Tell the
user that development provisioning can expire and may need renewal. Keep the
original and its data untouched. Do not present a development build as App Store
approved, permanent, or redistributable; if provisioning is blocked, report that
instead of handing over a noninstallable archive as a completed app.
