# Android — experimental, unverified

## Tools for this target

Run tools on the desktop host and check the [shared inventory](tools.md) first.
Distinguish APK resources, DEX bytecode, and native ELF libraries. They do not
share a single decompiler or rebuild path.

| Task | Tools and selection notes |
| --- | --- |
| SDK component discovery | [sdkmanager](https://developer.android.com/tools/sdkmanager) and [Android SDK tools](https://developer.android.com/tools). Select only needed host-compatible components, not all of Android Studio. |
| Package, manifest, and resource inspection | [apkanalyzer](https://developer.android.com/tools/apkanalyzer) and [AAPT2](https://developer.android.com/tools/aapt2) for APK contents/resources. |
| DEX decompilation | [JADX](https://github.com/skylot/jadx) for Java-like views of DEX. Decompiled output is for understanding, not a guarantee of recompilable original source. |
| Resources and bytecode changes | [Apktool](https://apktool.org/) for supported decode/rebuild workflows, [smali/baksmali](https://github.com/google/smali) for DEX assembly/disassembly. Work only on the copied authorized package. |
| Native disassembly and decompilation | [Ghidra](https://github.com/NationalSecurityAgency/ghidra) on the desktop host for native `.so` libraries. Use [PyGhidra](https://github.com/NationalSecurityAgency/ghidra/blob/master/Ghidra/Features/PyGhidra/README.md) if scripted Ghidra analysis is needed. |
| Python APK and native inspection | [Androguard](https://github.com/androguard/androguard) for APK/DEX structures. [LIEF](https://lief.re/), [pyelftools](https://github.com/eliben/pyelftools), and [Capstone](https://www.capstone-engine.org/) for native libraries and instructions. |
| Instruction assembly and bounded tests | [Keystone](https://www.keystone-engine.org/) or [LLVM tools](https://llvm.org/docs/CommandGuide/), plus [Unicorn](https://www.unicorn-engine.org/). CPU emulation does not supply Android framework APIs. |
| Small native additions and debugging | [Android NDK](https://developer.android.com/ndk) for matching native toolchains, [LLDB](https://lldb.llvm.org/) for permitted developer-build debugging. Match each required ABI and supported API level. |
| Alignment, signing, and verification | [zipalign](https://developer.android.com/tools/zipalign) and [apksigner](https://developer.android.com/tools/apksigner). Use the new app's own key and validate every APK in a split set. |
| App Bundle inputs | [bundletool](https://github.com/google/bundletool) for supported `.aab`/APK-set workflows. Do not treat an AAB as an installable APK or omit required splits. |
| Deployment and test environment | [ADB](https://developer.android.com/tools/adb) for user-approved device communication and logs. [Android Emulator](https://developer.android.com/studio/run/emulator) is an optional disposable test environment. |

Choose the selected tool's documented Java runtime only when needed. Android
Studio, an emulator image, and the NDK are separate optional downloads. Check
host OS/CPU compatibility and follow [Python environment rules](tools.md#python-packages).
None of these tools grants access to protected app data or bypasses device policy.

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
