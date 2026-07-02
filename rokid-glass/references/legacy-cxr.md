# Legacy Rokid CXR SDK (Non-Glass3)

Use this reference only when targeting **older Rokid AR glasses** (not Glass3).

## Glass3 vs Legacy

| | Glass3 (current) | Legacy CXR |
|--|------------------|------------|
| SDK artifacts | `glass3.open.sdk`, `phone.sdk` | CXR-M (mobile), CXR-S (on-device) |
| OS | YodaOS Android 12 | YodaOS variants on earlier hardware |
| Docs | https://x-docs.rokid.com | Community reverse-engineering |
| Protocol | Glass3 security service bus | CXR protocol over BT + Wi-Fi Direct |

**Default to Glass3 SDK** unless the user explicitly names older hardware (Rokid Air, Max, Station, etc.) or an existing CXR codebase.

## CXR Architecture (Legacy)

- **CXR-M SDK**: Android/iOS companion app on phone
- **CXR-S SDK**: On-device app on YodaOS-Sprite glasses
- Communication: Bluetooth + Wi-Fi Direct via CXR protocol suite

## Community Documentation

Reverse-engineered platform docs (hardware, services, CXR internals):
https://github.com/buildwithfenna/rokid-docs

Key facts from community analysis:
- Model identifier: `RG-glasses`
- ABI: `arm64-v8a`
- Android 12 (API 32), Qualcomm QSSI "Go" (low-RAM) config
- Sensors: InvenSense ICM-4x6xx IMU

## Migration Guidance

When porting legacy CXR apps to Glass3:

1. Replace CXR-M/CXR-S imports with `phone.sdk` / `glass3.open.sdk`
2. Reimplement init: `GlassSdk.bindSecurityService` + `PSecuritySDK.initSDK`
3. Map CXR data channels to Glass3 message/P2P services
4. Update `clientId` routing (new registration model)
5. Retest all cloud features with new AK/SK and `EngineParam` config

Do not assume API parity — verify each capability against Glass3 API reference.
