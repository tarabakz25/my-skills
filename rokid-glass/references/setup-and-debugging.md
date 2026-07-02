# Rokid Glass3 — Setup and Debugging

## Hardware

| Item | Purpose | Required |
|------|---------|----------|
| Glass3 **data debug cable** | adb, APK install, logcat | Required for dev |
| Glass3 **charging cable** | Power only — no adb | Do not use for debugging |
| Android phone | Companion app testing | Required for two-device features |
| scrcpy | Mirror glasses display to desktop | Strongly recommended |

### Confirm glasses in adb

```bash
adb devices
# Expected: Rokid RG-glasses    device
```

If the device is missing:
1. Swap to the data debug cable.
2. Enable USB debugging on glasses (usually pre-enabled on dev builds).
3. Revoke and re-authorize USB debugging if prompted.

### scrcpy

Mirror the glasses screen to verify UI and interactions:

```bash
scrcpy -s Rokid
# or select by serial from adb devices
```

Docs: https://x-docs.rokid.com/docs/en/resources/

## Development Environment

| Item | Requirement |
|------|-------------|
| Android Studio | 2022 or later |
| JDK | 17+ |
| Android SDK | 34 recommended (Demo target) |
| Gradle | Match Demo project (typically 7.x–8.x) |
| Glasses OS | YodaOS / Android 12 (API 32) |
| Phone min SDK | Android 8.0 (API 26) |

## Permissions

### Phone-side manifest (common)

```xml
<!-- Network -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
<uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_WIFI_STATE" />
<uses-permission android:name="android.permission.CHANGE_NETWORK_STATE" />

<!-- Media -->
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.RECORD_AUDIO" />
<uses-permission android:name="android.permission.VIBRATE" />

<!-- Storage -->
<uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
<uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />

<!-- Bluetooth (pre-Android 12) -->
<uses-permission android:name="android.permission.BLUETOOTH" />
<uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />

<!-- Bluetooth (Android 12+) -->
<uses-permission
    android:name="android.permission.BLUETOOTH_SCAN"
    android:usesPermissionFlags="neverForLocation" />
<uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
<uses-permission android:name="android.permission.BLUETOOTH_ADVERTISE" />

<!-- Location + Wi-Fi P2P -->
<uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
<uses-permission
    android:name="android.permission.NEARBY_WIFI_DEVICES"
    android:usesPermissionFlags="neverForLocation" />

<uses-feature android:name="android.hardware.wifi.direct" android:required="false" />
<uses-feature android:name="android.hardware.camera" android:required="false" />
```

### Glasses-side additions

Glasses apps also need `MANAGE_EXTERNAL_STORAGE` for some file operations:

```xml
<uses-permission
    android:name="android.permission.MANAGE_EXTERNAL_STORAGE"
    tools:ignore="AllFilesAccessPolicy,ScopedStorage" />
```

Request dangerous permissions at runtime on both sides.

## Demo Run Order

1. Build phone Demo: `cd glass3sdkphonedemo && ./gradlew assembleDebug`
2. Build glasses Demo: `cd glassdemo && ./gradlew assembleDebug`
3. Install and launch **phone** Demo on Android phone
4. Connect glasses via data debug cable; install and launch **glasses** Demo
5. From phone: scan and connect to Glass3
6. Grant all permission prompts on both devices

### Demo authentication

`UserAuthInfo("", "")` in `MainPhoneActivity` is a placeholder. Fill real AK/SK before testing online ASR/TTS/AI.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| adb shows no glasses | Charging cable, not debug cable | Use Glass3 data debug cable |
| `GlassSdk.isReady()` false | Service not bound | Call `bindSecurityService`; check logs for bind errors |
| Phone `isInit()` false | Missing or invalid `EngineParam` | Verify `initSDK` callback; check AK/SK if cloud enabled |
| Bluetooth scan empty | Permissions not granted | Grant Bluetooth + location runtime permissions |
| P2P fails after BT connect | Wi-Fi permissions or timing | Grant NEARBY_WIFI_DEVICES; wait for BT stable before P2P |
| Messages not received | `clientId` mismatch | Align phone `clientIds` with glasses `registerClient` |
| ASR/TTS silent failure | Empty AK/SK | Request credentials from Rokid BizDev |
| Duplicate native lib build error | `libr2aud.so` conflict | Add `packagingOptions.pickFirst` in glasses module |

### FAQ links

- Bluetooth: https://x-docs.rokid.com/docs/en/faq/%E8%93%9D%E7%89%99%E9%97%AE%E9%A2%98%E6%8E%92%E6%9F%A5.html
- P2P: https://x-docs.rokid.com/docs/en/faq/P2P%E9%97%AE%E9%A2%98%E6%8E%92%E6%9F%A5.html
- General: https://x-docs.rokid.com/docs/en/faq/%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98.html

## Useful adb Commands

```bash
# Device list
adb devices

# Glasses logcat (filter SDK tags)
adb -s <glasses-serial> logcat -s GlassSdk PSecuritySDK SDK_CHECK

# Install glasses APK
adb -s <glasses-serial> install -r app-debug.apk

# Screenshot from glasses
adb -s <glasses-serial> exec-out screencap -p > glass-screen.png
```
