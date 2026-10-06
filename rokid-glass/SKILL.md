---
name: rokid-glass
description: "Use when building Android apps for Rokid Glass3 (glasses-side or phone companion) with Glass3 SDK — device pairing, P2P messaging, media, speech/AI, vision, and YodaOS debugging. Covers Maven setup, two-side initialization, clientId matching, permissions, and scrcpy debugging."
disable-model-invocation: true
version: 1.0.0
author: kz
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [rokid, glass3, android, ar, wearable, yodaos]
    related_skills: [android-clean-architecture, accessibility, e2e-testing]
---

# Rokid Glass Development

## Overview

Rokid Glass3 runs **YodaOS** (Android 12, API 32) on-device. The **Glass3 SDK** (`glass3.open.sdk` on glasses, `phone.sdk` on phone) enables two-device Android apps: phone companion controls glasses over Bluetooth + Wi-Fi P2P, while glasses apps call hardware capabilities (camera, mic, display, sensors).

**Core architecture**: Phone scans/connects via classic Bluetooth → negotiates P2P → exchanges messages, files, and AV streams. Glasses do not reach the public internet directly; traffic relays through the phone:

```
Glasses → P2P → Phone → Cellular/Wi-Fi → Server → Phone → P2P → Glasses
```

Official docs: https://x-docs.rokid.com/docs/en/terminal-sdk/getting-started/

## When to Use

**Use this skill when:**
- Creating or modifying Rokid Glass3 glasses-side or phone companion Android apps
- Integrating Glass3 SDK (connectivity, messaging, media, ASR/TTS, AI chat, vision)
- Debugging device recognition, Bluetooth, P2P, or SDK initialization failures
- Designing glasses-side UI within Glass3 display constraints
- Setting up the official Demo or cloning capability samples

**Don't use for:**
- Generic Android development without Glass3 SDK → use `android-clean-architecture`
- Legacy Rokid devices (Air, Max, Station) using CXR-M/CXR-S SDK — different APIs; see [references/legacy-cxr.md](references/legacy-cxr.md)
- YodaOS voice IoT (Linux/Node.js) — unrelated to Glass3 Android stack

## Platform Quick Reference

| Item | Value |
|------|-------|
| Device | Rokid Glass3 (`Rokid RG-glasses` in adb) |
| OS | YodaOS on Android 12 (SDK 32), arm64-v8a |
| Glasses SDK | `com.rokid.security:glass3.open.sdk` |
| Phone SDK | `com.rokid.security:phone.sdk` |
| JDK | 17+ |
| Android Studio | 2022+ |
| Phone target | Android 8.0+ (SDK 26+) |
| Demo repo | https://gitee.com/as_pixar/glass3sdkdemo |

Pin SDK versions to match the Demo or docs (e.g. `2.2.0-E`). Check Maven for newer releases before upgrading.

## Two-Side Project Layout

Glass3 apps are **two independent Android projects** (or two modules with separate manifests):

```
rokid-app/
├── phone-app/          # Companion: scan, connect, P2P, relay, control
│   └── depends on phone.sdk
└── glass-app/          # On-glasses: UI, hardware, receive commands
    └── depends on glass3.open.sdk
```

| Side | Entry class (Demo) | SDK entry |
|------|-------------------|-----------|
| Phone | `com.rokid.phone.ui.MainPhoneActivity` | `PSecuritySDK` |
| Glasses | `com.rokid.glass.HomeActivity` | `GlassSdk` |

**Critical**: `clientId` strings must match across sides. Phone `EngineParam.clientIds` must include every glasses app `registerClient()` id.

## Integration Workflow

### 1. Environment and hardware

1. Install Android Studio with **JDK 17**, Android SDK 34.
2. Use the **Glass3 data debug cable** (not the charging-only cable) to connect glasses to the dev machine.
3. Verify `adb devices` shows `Rokid RG-glasses`.
4. Install **scrcpy** to mirror the glasses display during development.

Details: [references/setup-and-debugging.md](references/setup-and-debugging.md)

### 2. Maven repository

Gradle 7.0+ — add to `settings.gradle`:

```groovy
dependencyResolutionManagement {
    repositories {
        google()
        mavenCentral()
        maven { url 'https://maven.rokid.com/repository/maven-public/' }
    }
}
```

### 3. Dependencies

**Glasses module** (`build.gradle`):

```groovy
dependencies {
    implementation('com.rokid.security:glass3.open.sdk:2.2.0-E') {
        exclude group: "org.slf4j"
    }
}

android {
    packagingOptions {
        pickFirst 'lib/arm64-v8a/libr2aud.so'
        pickFirst 'lib/armeabi-v7a/libr2aud.so'
    }
}
```

**Phone module**:

```groovy
dependencies {
    implementation('com.rokid.security:phone.sdk:2.2.0-E') {
        exclude group: "org.slf4j"
    }
}
```

### 4. Permissions

Declare manifest permissions per capability (Bluetooth, Wi-Fi P2P, camera, mic, storage, location). Request dangerous permissions at runtime on Android 6+.

Full permission blocks: [references/setup-and-debugging.md#permissions](references/setup-and-debugging.md)

### 5. SDK initialization

**Glasses side** — bind system service, then register client:

```kotlin
fun initGlassSdk(context: Context, clientId: String, callback: IClientCallback) {
    if (GlassSdk.isReady()) return
    GlassSdk.bindSecurityService(context, object : IServiceConnectionCallback {
        override fun onServiceConnected() {
            GlassSdk.registerClient(clientId, callback)
        }
        override fun onServiceDisconnected() { /* reconnect */ }
        override fun onBindingDied() { /* rebind */ }
    })
}
```

**Phone side** — initialize engine with matching client IDs and credentials:

```kotlin
fun initPhoneSdk(
    clientIds: List<String>,       // e.g. listOf("SecurityPhone", "GlassSample")
    appId: String,
    secret: String,
    onResult: (Boolean) -> Unit
) {
    val param = EngineParam(
        clientIds = ArrayList(clientIds),
        userAuthInfo = UserAuthInfo(appId, secret),
        envType = EnvType.PUBLIC,
        banServiceList = arrayListOf(NetServiceType.ALL) // skip cloud until needed
    )
    PSecuritySDK.initSDK(param) { result ->
        onResult(result.isSuccess)
    }
}
```

- `UserAuthInfo` AK/SK: request from Rokid BizDev for online ASR/TTS/AI.
- `banServiceList = ALL` skips optional cloud bootstrap during local dev.
- Remove `ALL` ban when enabling ASR, TTS, translate, or RTC.

### 6. Verify initialization

```kotlin
// Glasses
Log.d("SDK_CHECK", "glass sdk ready = ${GlassSdk.isReady()}")

// Phone
Log.d("SDK_CHECK", "phone sdk initialized = ${PSecuritySDK.getMobileEngineService().isInit()}")
```

Both should log `true` before calling capability services.

### 7. Obtain capability services

Always guard with `isReady()` / `isInit()` — services return null when uninitialized.

```kotlin
// Glasses
val messageService = GlassSdk.getGlassMessageService()
val mediaService = GlassSdk.getGlassMediaService()
val asrService = GlassSdk.getGlassAsrService()

// Phone
val btService = PSecuritySDK.getClassicBlueToothClientService()
val p2pService = PSecuritySDK.getWifiP2PClientService()
val messageService = PSecuritySDK.getMessageService()
```

Service map: [references/sdk-api.md](references/sdk-api.md)

### 8. Connection flow (phone → glasses)

1. Phone: classic Bluetooth scan and connect.
2. Both sides: establish Wi-Fi P2P channel.
3. Exchange messages/files over P2P.
4. For cloud APIs: phone forwards requests; glasses receive responses via P2P.

Run phone Demo first, then glasses Demo. Grant Bluetooth, Wi-Fi/Nearby, camera, mic, storage, and notification listener on first launch.

## Capability Areas

| Area | Glasses service | Phone service | Notes |
|------|----------------|---------------|-------|
| Messaging | `getGlassMessageService()` | `getMessageService()` | Text, files, notifications |
| Media | `getGlassMediaService()` | via message/P2P | Photo, video, live preview |
| ASR/TTS | `getGlassAsrService()`, `getGlassTtsService()` | engine relay | Requires AK/SK for online |
| AI Chat | `getGlassAiChatService()` | engine relay | Cloud credentials |
| Offline voice | `getGlassOfflineCmdService()` | — | On-device command words |
| Vision | `getGlassTrackService()`, `getGlassOnlineRecService()` | — | Face, plate, person/vehicle |
| Bluetooth ring | `getGlassBluetoothRingService()` | `getBluetoothRingService()` | Optional peripheral |
| Device state | `getGlassDeviceService()` | connection monitors | Battery, visibility |

Code samples by capability: https://x-docs.rokid.com/docs/en/downloads/samples.html

## Glasses UI Guidelines

Before building glasses-side UI, read the [Glasses UI guidelines](https://x-docs.rokid.com/docs/en/terminal-sdk/capabilities/%E8%AE%BE%E8%AE%A1%E8%A7%84%E8%8C%83.html):

- Design for the **limited display area** and monocular viewing distance.
- Use **large touch targets** and high contrast; minimize dense text.
- Respect **safe margins** — keep critical content away from edges.
- Prefer **single-focus screens**; avoid multi-column layouts.
- Test on-device with scrcpy, not only phone emulators.

## Demo-First Development

Clone and run the official Demo before writing custom code:

```bash
git clone https://gitee.com/as_pixar/glass3sdkdemo.git
cd glass3sdkdemo/glassdemo && ./gradlew assembleDebug
cd ../glass3sdkphonedemo && ./gradlew assembleDebug
```

Verification order:

| Step | Capability | Pass criteria |
|------|------------|---------------|
| 1 | SDK init | Both sides `true` in SDK_CHECK logs |
| 2 | Bluetooth | Phone scans and connects to Glass3 |
| 3 | Messaging | Text exchange phone ↔ glasses |
| 4 | File transfer | Small file round-trip |
| 5 | P2P | Channel established for AV/large files |
| 6 | Media | Photo/video or live preview works |

## Development Patterns

### Network relay pattern

Glasses apps needing REST/GraphQL should **not** open direct internet connections. Implement API calls on the phone; forward request/response payloads over the message or P2P channel.

### Service lifecycle

- Glasses: call `GlassSdk.release()` when the app exits or SDK is no longer needed.
- Phone: call `PSecuritySDK.destroySDK()` to release engine resources.
- Handle `onServiceDisconnected` / `onBindingDied` on glasses with rebind logic.

### Error handling

- Null-check every `getGlassXxxService()` / `getXxxService()` return.
- Log and surface connection state before retrying operations.
- For Bluetooth/P2P failures, consult Rokid FAQ before changing app logic.

## Common Pitfalls

1. **Using the charging cable for debugging** — Glasses charge but adb sees no device. Use the Glass3 **data debug cable**.

2. **Mismatched `clientId`** — Phone `clientIds` must include the exact string passed to `GlassSdk.registerClient()`. Mismatch = messages routed to wrong app or dropped.

3. **Calling services before init** — `getGlassXxxService()` returns null if `isReady()` / `isInit()` is false. Always verify first.

4. **Expecting glasses internet access** — Route cloud traffic through the phone P2P relay.

5. **Missing runtime permissions** — Manifest alone is insufficient for Bluetooth (12+), location (P2P), camera, mic, storage.

6. **Empty AK/SK with online speech** — ASR/TTS/AI Chat need real `UserAuthInfo` credentials. Placeholder `("", "")` works for local connectivity only.

7. **Native library conflicts** — Add `pickFirst` for `libr2aud.so` if Gradle reports duplicate native libs.

8. **Running glasses Demo before phone Demo** — Start phone side first so Bluetooth pairing and client registration succeed.

9. **Designing UI from phone screen dimensions** — Glass3 has a small monocular display; follow glasses UI guidelines.

10. **Mixing SDK versions** — Keep glasses and phone SDK artifact versions aligned.

## Verification Checklist

- [ ] Glass3 data debug cable connected; `adb devices` lists glasses
- [ ] scrcpy mirrors glasses display
- [ ] Rokid Maven repo configured; both SDK deps resolve
- [ ] Manifest permissions declared; runtime permissions granted
- [ ] `clientId` matches on phone `EngineParam` and glasses `registerClient`
- [ ] `GlassSdk.isReady()` and phone `isInit()` both `true`
- [ ] Bluetooth connect succeeds from phone Demo
- [ ] P2P channel established; message round-trip works
- [ ] Glasses UI tested on-device (not emulator-only)
- [ ] Cloud features have valid AK/SK when enabled

## References

| File | Content | When to Read |
|------|---------|--------------|
| [references/setup-and-debugging.md](references/setup-and-debugging.md) | Cables, scrcpy, permissions, FAQ links | Setup and debugging |
| [references/sdk-api.md](references/sdk-api.md) | Service entry points, EngineParam fields | API lookup during implementation |
| [references/legacy-cxr.md](references/legacy-cxr.md) | CXR-M/CXR-S for older Rokid devices | Non-Glass3 hardware |

External docs:
- Overview: https://x-docs.rokid.com/docs/en/terminal-sdk/getting-started/
- Glasses API: https://x-docs.rokid.com/docs/en/terminal-sdk/api-reference/
- Phone API: https://x-docs.rokid.com/docs/en/terminal-sdk/api-reference/
- FAQ: https://x-docs.rokid.com/docs/en/faq/
