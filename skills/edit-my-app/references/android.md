# Android — experimental, unverified

## Tools for this target

Check [Android SDK tools](https://developer.android.com/tools), including ADB,
apksigner, and [zipalign](https://developer.android.com/tools/zipalign), before
downloading them. [JADX](https://github.com/skylot/jadx) can inspect DEX bytecode;
[Apktool](https://apktool.org/) handles package resources/bytecode workflows.
Choose compatible releases and their documented Java runtimes only as needed.
Android Studio, an emulator image, and the NDK are separate optional downloads,
not prerequisites for every change. Downloads must match the desktop host OS/CPU.

## Confirm a supported input

Ask which app and device, and whether the user has an authorized APK or developer
build. An app name is enough to begin discovery; do not expect package-name
knowledge. Prefer a user-supplied package or an official developer artifact.
Do not extract private data, remove DRM, root a device, or bypass integrity checks.

Record the package/application ID, ABI, SDK requirements, signing identity, and
whether this is a complete APK, split APK set, or an app bundle. A base APK alone
may not run; do not pretend an `.aab` is a directly installable APK. Stop when
required splits, permissions, or authorized unprotected artifacts are missing.

## Copy and change the smallest part

Preserve the complete input package/set as an untouched baseline. Work on a
separate copy. Inspect resources/manifest and, only as needed, bytecode/native
components with the tools catalog. A decompiler's output is not the app's original
source. Resource changes, supported extension points, or narrow bytecode/native
additions should reuse the existing product rather than reimplement it.

Use a distinct app label, icon, and application ID for side-by-side installation.
Check manifest components, provider authorities, permissions, deep links, native
references, backend identity, and signature-bound APIs. Blindly replacing a
package-name string is not a reliable cloning strategy. Some apps will not run
with another ID or signing key; explain the blocker instead of removing checks.

## Local signing and device consent

Use a new project-owned signing key stored securely outside the app/repository.
Android updates normally need compatible signing identity; a new local key is
not permission to replace the original. Never uninstall the original to resolve
a signature mismatch. Follow [Android signing guidance](https://developer.android.com/studio/publish/app-signing).

Use current supported build tools for alignment and signing; finalize package
contents before signing, and run [apksigner verification](https://developer.android.com/tools/apksigner)
on every output APK. All installed splits need compatible identities/signatures.
Check the device's current installation/developer-verification requirements
rather than promising unrestricted sideloading on every device or region.

Prefer a disposable emulator first when suitable. For a physical device, explain
the specific supported installation route. The user handles USB debugging and
the device's authorization prompt if [ADB](https://developer.android.com/tools/adb)
is needed, or approves the selected app-install source in normal Settings.
Do not disable Play Protect or bypass enterprise/device policy. Check SDK tools
already installed on the host before requesting downloads.

## Deliver the visible clone

Install only the distinctly identified clone through the approved route. Verify
its icon in the launcher and test launch, the requested behavior, permissions,
and existing functions with disposable data. Emulator success is not physical
device verification. Retain a previous signed clone for rollback; protect the key
needed for future clone updates. Tell the user how to remove only the new app.
The generated app is not Play-approved or distribution-ready, and the original
app's license still applies to copied code/resources.
