Solar Panel for UPM STEM IoT 2026.

This repository is to update and fallback to if my server code or any other code doesn't work.
This code will be updated and put in releases.
The code in the source code is version 1.0
Older versions do not exist.
Here is the list of updates until this version.

Format: version codename - updates

v0.1 Alpha - • application was made
v0.2 Beta - v0.3 Gamma • resolve json error
v0.4 Delta - • resolve mit app errors and addrd some decoration
v0.5 Epsilon - • added press back button to exit app dialog
v0.6 Zeta - BIG UPDATE!
         • added verification
         • kept ip in tinydb to store while using app
         • made close_screen_with_start_val use data from tinydb instead of the textbox
         • changed the password text box to text box for easy viewing
         • rounded off the slider input
         • made verification code global for easy handling using self.__class__.variable
         • made verification work 
v0.7 Ena - BIG UPDATE!
         • changed version label
         • fixed few bugs
         • hides only servox and servoy label and sliders if manual control switch is off
         • updated server to run on esp32-wroom
v0.8 Theta - MEGA UPDATE!
         • changed mockdata to data recieved from sliders and switches
         • fixed bug where s1,s2,sw1,and sw2 weren't declared in global list
         • fixed massive bug where server couldnt recieve post updates, sync coordinates globally in memory,
           threw random json errors and wouldnt load..
         • made the json data update! (FINALLY)
v0.9 Iota - HUGE UPDATE!
         • ported everything to run on both PC and ESP32 when needed...
         • added wifi auto-connect
         • stopped the server from freezing while waiting for ping
         • upgraded bare esp32 sockets into active data streams
         • added content-length target header parsing
         • added sensor i/o's (fc37 and guva)
         • used algorithm for the single UV sensor
         • added captive portal wifi manager
         • added timer matrix that checks sky.. if uv drop below shadow threshold for 
           15mins, put panel in neutral position
         • added inactivity tracker
v1.0 Kappa - BIG UPDATE!
         • added custom html file as wifi portal

Fallback WiFi code:

# def connect_wifi():
#     """Attempts to connect to saved Wi-Fi; falls back to Captive Portal on failure."""
#     config_file = "wifi_config.json"
    
#     # Check if we have saved settings from a previous session
#     if config_file in os.listdir():
#         try:
#             with open(config_file, "r") as f:
#                 cfg = json.loads(f.read())
            
#             print(f"[WIFI]: Found saved credentials for {cfg['ssid']}")
#             wlan = network.WLAN(network.STA_IF)
#             wlan.active(True)
#             wlan.connect(cfg['ssid'], cfg['password'])
            
#             # Wait up to 10 seconds to connect
#             for _ in range(20):
#                 if wlan.isconnected():
#                     print("[WIFI]: Connected! IP:", wlan.ifconfig()[0])
#                     return True
#                 time.sleep(0.5)
#             print("[WIFI]: Connection timed out. Booting configuration portal...")
#         except Exception as e:
#             print("[WIFI ERROR]: Config read failed:", e)
            
#     # If no config exists, or connection failed, launch the Portal setup
#     start_captive_portal()
#     return False

# def start_captive_portal():
#     """Broadcasts a setup Wi-Fi network and serves a credential entry form."""
#     ap = network.WLAN(network.AP_IF)
#     ap.active(True)
#     # The Wi-Fi hotspot name that shows up on your phone
#     ap.config(essid="Solar-Tracker-Setup", authmode=network.AUTH_OPEN)
    
#     print("[PORTAL]: Hotspot 'Solar-Tracker-Setup' is active on 192.168.4.1")
    
#     # Simple Setup Webpage HTML string
#     portal_html = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
#     <html>
#     <head><meta name="viewport" content="width=device-width, initial-scale=1"></head>
#     <body style="font-family:Arial; text-align:center; padding:20px;">
#         <h2>Solar Tracker Wi-Fi Setup</h2>
#         <form action="/save" method="POST">
#             SSID:<br><input type="text" name="ssid" required><br><br>
#             Password:<br><input type="password" name="password" required><br><br>
#             <input type="submit" value="Save & Restart Settings" style="padding:10px 20px;">
#         </form>
#     </body>
#     </html>"""

#     # Set up a quick port 80 portal socket server
#     portal_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     portal_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     portal_socket.bind(('0.0.0.0', 80))
#     portal_socket.listen(1)

To add a camera:
Add in MIT AI2:

when Web1.GotText (url, responseCode, responseType, responseContent) do
    if get responseCode = 200 then
        # 1. Parse your incoming data string into a standard App Inventor dictionary
        set local responseDict to call JsonTextDecodeWithDictionaries (get responseContent)
        
        # 2. Extract and assign your existing tracking values to your labels/sliders
        set Label_ServoX.Text to call JsonObjectByPath (list: "servo_x", get responseDict)
        set Label_ServoY.Text to call JsonObjectByPath (list: "servo_y", get responseDict)
        
        # 3. Extract the new streaming string and instantly push it to your video layout frame
        set WebViewer1.HomeUrl to call JsonObjectByPath (list: "video_url", get responseDict)
        call WebViewer1.GoToUrl (url: get WebViewer1.HomeUrl)
