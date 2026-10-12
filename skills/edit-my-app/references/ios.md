# iOS / iPadOS — experimental, unverified

## Tools for this target

Use an existing compatible [Xcode installation](https://developer.apple.com/xcode/)
on the Mac host for its device/simulator SDKs, signing, and deployment tools.
Mac command-line tools alone are not an iOS SDK. Static inspection may use
`otool` or the shared optional analyzers; do not download a mobile exploitation
toolkit. Store/index tools by the host OS, not under an invented iOS tools path.

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
