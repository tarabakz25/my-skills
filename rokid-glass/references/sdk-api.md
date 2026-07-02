# Rokid Glass3 SDK — API Quick Reference

Official API docs:
- Glasses: https://x-docs.rokid.com/docs/en/terminal-sdk/api-reference/
- Phone: https://x-docs.rokid.com/docs/en/terminal-sdk/api-reference/

## GlassSdk Entry (Glasses Side)

| Method | Description |
|--------|-------------|
| `bindSecurityService(context, callback)` | Bind YodaOS security service |
| `registerClient(clientId, callback)` | Register app; `clientId` must match phone |
| `isReady()` | True when service bound and client registered |
| `release()` | Release SDK resources on app exit |

### Capability services (`getGlassXxxService()`)

| Method | Interface | Capability |
|--------|-----------|------------|
| `getClassicBluetoothService()` | `IBTService` | Classic Bluetooth |
| `getP2PGoService()` | `IWifiP2PGoService` | Wi-Fi P2P (glasses as GO) |
| `getGlassMessageService()` | `IMessageServer` | Messages and file transfer |
| `getGlassCommonService()` | `ICommonInfoServer` | User info, companion app info |
| `getGlassMediaService()` | `IMediaServer` | Photo, video, AV preview |
| `getGlassAsrService()` | `IAsrService` | Online ASR |
| `getGlassTtsService()` | `ITtsService` | Online TTS |
| `getGlassOfflineTtsService()` | `IOfflineTtsService` | Offline TTS |
| `getGlassOfflineCmdService()` | `IOfflineCmdService` | Offline voice commands |
| `getGlassAiChatService()` | `IAiChatService` | AI chat |
| `getGlassTrackService()` | `ITrackService` | Person/vehicle detection |
| `getGlassOnlineRecService()` | `IOnlineRecService` | Online recognition |
| `getGlassOfflineRecService()` | `IOfflineRecServer` | Offline recognition |
| `getGlassOfflineFeatureRecService()` | `IOfflineFeatureRecService` | Offline feature recognition |
| `getGlassIdentificationService()` | `IIdentificationService` | Identification |
| `getGlassFileSystemService()` | `IFileSystemService` | File upload/status |
| `getGlassDeviceService()` | `IDeviceService` | Battery, system events |
| `getGlassNotificationService()` | `INotificationService` | Notifications |
| `getGlassBluetoothRingService()` | `IBluetoothRingService` | Bluetooth ring |
| `getGlassTranslateService()` | `ITranslateService` | Translation |
| `getGlassCollectService()` | `ICollectService` | Image collection |

**Pattern**: Always check `GlassSdk.isReady()` before calling; handle null returns.

```kotlin
if (!GlassSdk.isReady()) return
val media = GlassSdk.getGlassMediaService() ?: return
```

## PSecuritySDK Entry (Phone Side)

| Method | Returns | Description |
|--------|---------|-------------|
| `initSDK(param, onResult)` | — | Initialize phone engine |
| `destroySDK()` | — | Release engine |
| `getMobileEngineService()` | `IMobileEngine` | Core engine; check `isInit()` |
| `getClassicBlueToothClientService()` | `IClassicBluetoothClient` | BT scan/connect |
| `getWifiP2PClientService()` | `IWifiP2PClientOperate` | P2P client |
| `getMessageService()` | `IMessage` | Messages and files |
| `getBluetoothRingService()` | `IBluetoothRing` | Bluetooth ring |
| `getOtaEngineService()` | OTA engine | Firmware updates |

## EngineParam (Phone Init)

```kotlin
data class EngineParam(
    var clientIds: ArrayList<String>? = null,      // Must include glasses clientId(s)
    var userAuthInfo: UserAuthInfo? = null,        // AK/SK from Rokid BizDev
    var envType: String,                           // EnvType.PUBLIC or CUSTOM
    var customHost: String? = null,                 // Required when envType = CUSTOM
    var banServiceList: List<NetServiceType>? = null
)
```

### banServiceList values

| Value | Effect |
|-------|--------|
| `NetServiceType.ALL` | Skip all optional cloud service init (good for local dev) |
| `NetServiceType.TranslateService` | Skip translate bootstrap |
| `NetServiceType.RtcService` | Skip RTC bootstrap |
| `null` or empty | Initialize all configured cloud services |

Remove `ALL` ban when enabling ASR, TTS, translate, or RTC.

## clientId Convention (Demo)

```kotlin
// Phone
val clientIds = arrayListOf("SecurityPhone", "GlassSample")

// Glasses (must match an entry in phone clientIds)
GlassSdk.registerClient("GlassSample", callback)
```

- `SecurityPhone` — system-level phone identifier
- `GlassSample` — app-level glasses identifier
- Add one `clientId` per distinct glasses app that receives routed messages

## Speech / AI Data Flow

| Capability | Flow |
|------------|------|
| Online ASR | Glasses mic → P2P → phone → speech cloud → result → P2P → glasses |
| Online TTS | Glasses text → P2P → phone → speech cloud → audio → P2P → glasses |
| AI Chat | Glasses prompt → P2P → phone → AI service → response → glasses |

Private ASR/TTS deployment: https://x-docs.rokid.com/docs/en/private-speech/SDK_INTEGRATION.html

## QR Scan SDK (Separate)

QR scanning uses a separate SDK — not part of `glass3.open.sdk`:
https://x-docs.rokid.com/docs/en/scan/

## Code Samples by Capability

https://x-docs.rokid.com/docs/en/downloads/samples.html

Categories: connectivity, messaging, media, speech/AI, vision, system settings, OTA.
