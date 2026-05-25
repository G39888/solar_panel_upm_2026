# Solar Panel for UPM STEM IoT 2026

This repository serves as the central codebase and fallback hub for the UPM STEM IoT 2026 Solar Panel tracking project. The source code reflects version 1.0. Stable builds are packaged and available under the **Releases** section.

---

## 📑 Changelog

The development journey and updates up to the current version:


| Version | Codename | Key Updates |
| :--- | :--- | :--- |
| **v0.1** | Alpha | • Initial application creation. |
| **v0.2** | Beta | • Baseline testing and minor stabilization. |
| **v0.3** | Gamma | • Resolved JSON parsing errors. |
| **v0.4** | Delta | • Fixed MIT App Inventor integration errors; added UI decorations. |
| **v0.5** | Epsilon | • Implemented a confirmation dialog on pressing the back button to exit the app. |
| **v0.6** | Zeta | **BIG UPDATE!** <br>• Added verification mechanisms.<br>• Persisted IP addresses in `TinyDB` during active app use.<br>• Configured `close_screen_with_start_val` to pull data from `TinyDB` instead of raw textboxes.<br>• Changed the password textbox configuration for easier viewing.<br>• Rounded off slider inputs.<br>• Made verification codes global via `self.class.variable`. |
| **v0.7** | Ena | **BIG UPDATE!** <br>• Updated version label metrics.<br>• Fixed minor bugs.<br>• Dynamically hides Servo X/Y labels and sliders if the manual control switch is toggled off.<br>• Upgraded server compatibility to run natively on the ESP32-WROOM. |
| **v0.8** | Theta | **MEGA UPDATE!** <br>• Substituted mock data with real-time feedback from sliders and switches.<br>• Patched a critical bug where `s1`, `s2`, `sw1`, and `sw2` missed global declaration updates.<br>• Fixed an issue preventing the server from receiving POST requests, syncing global memory coordinates, and throwing JSON loading errors.<br>• Enabled dynamic JSON data updates. |
| **v0.9** | Iota | **HUGE UPDATE!** <br>• Ported code structure to run interchangeably on PC environments and ESP32 hardware.<br>• Integrated Wi-Fi auto-connect logic.<br>• Optimized network loops to stop server freezing while awaiting ping blocks.<br>• Upgraded bare ESP32 sockets into active data streams.<br>• Added explicit parsing for `Content-Length` target headers.<br>• Built-in sensor I/O protocols (FC37 and GUVA).<br>• Applied tracking optimization algorithms for single UV sensors.<br>• Built-in captive portal Wi-Fi network manager.<br>• Added a timer matrix rule: if UV metrics drop below shadow thresholds for 15 minutes, the panel resets to a neutral position.<br>• Added an inactivity tracking loop. |
| **v1.0** | Kappa |• Refactored the network manager to load custom external HTML template files as the dedicated Wi-Fi captive portal landing screen. |
| **v1.1** | Lambda | **CURRENT STABLE RELEASE** <br>• • Gave title text and the screen layout colour an overhaul. |

---

## 🛠 Network Management & Fallback Setup

The ESP32 firmware features an automatic fallback network sequence. If saved configurations fail, the board spins up an ad-hoc Access Point (AP) captive portal for provisioning.

```python
def connect_wifi():
    """Attempts to connect to saved Wi-Fi; falls back to Captive Portal on failure."""
    config_file = "wifi_config.json"
    
    # Check if we have saved settings from a previous session
    if config_file in os.listdir():
        try:
            with open(config_file, "r") as f:
                cfg = json.loads(f.read())
            print(f"[WIFI]: Found saved credentials for {cfg['ssid']}")
            
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)
            wlan.connect(cfg['ssid'], cfg['password'])
            
            # Wait up to 10 seconds to connect
            for _ in range(20):
                if wlan.isconnected():
                    print("[WIFI]: Connected! IP:", wlan.ifconfig()[0])
                    return True
                time.sleep(0.5)
            print("[WIFI]: Connection timed out. Booting configuration portal...")
        except Exception as e:
            print("[WIFI ERROR]: Config read failed:", e)
            
    # If no config exists, or connection failed, launch the Portal setup
    start_captive_portal()
    return False

def start_captive_portal():
    """Broadcasts a setup Wi-Fi network and serves a credential entry form."""
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    
    # The Wi-Fi hotspot name that shows up on your phone
    ap.config(essid="Solar-Tracker-Setup", authmode=network.AUTH_OPEN)
    print("[PORTAL]: Hotspot 'Solar-Tracker-Setup' is active on 192.168.4.1")
    
    # Simple Setup Webpage HTML string
    portal_html = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
    Solar Tracker Wi-Fi Setup
    SSID:<br><input type='text' id='ssid'><br>
    Password:<br><input type='password' id='pw'><br>
    """
    
    # Set up a quick port 80 portal socket server
    portal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    portal_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    portal_socket.bind(('0.0.0.0', 80))
    portal_socket.listen(1)
```

---

## Camera Extension (MIT App Inventor Integration)

To extend this application with a live video stream, integrate the following logical workflow into your **MIT AI2 Designer Blocks**:

### Block Logic Flowchart
```text
when Web1.GotText (url, responseCode, responseType, responseContent) do:
    if responseCode == 200 then:
        1. Parse incoming data string into an App Inventor dictionary:
           set local responseDict -> call JsonTextDecodeWithDictionaries(responseContent)
        
        2. Extract tracking coordinates and map them to UI elements:
           set Label_ServoX.Text  -> call JsonObjectByPath(["servo_x"], responseDict)
           set Label_ServoY.Text  -> call JsonObjectByPath(["servo_y"], responseDict)
        
        3. Extract the target streaming video URL and display it on the layout frame:
           set WebViewer1.HomeUrl -> call JsonObjectByPath(["video_url"], responseDict)
           call WebViewer1.GoToUrl(WebViewer1.HomeUrl)
```
