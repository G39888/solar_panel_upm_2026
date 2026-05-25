import socket  # import usocket as socket  # Comment out for PC
import json    # import ujson as json  #Comment out too for PC 
import random  # import urandom as random #Comment out too for PC
import sys
# import network
# import os
# import time
# import machine
# from machine import PWM, Pin, ADC

# ---- Servos ----
# servo_x = PWM(Pin(18), freq=50)
# servo_y = PWM(Pin(19), freq=50)

# --- Rain Sensor (FC-37) Setup ---
# rain_sensor = ADC(Pin(32))     # Connected to Safe ADC1 pin
# rain_sensor.atten(ADC.ATTN_11DB) # Allows full 0V - 3.3V reading range

# --- UV Tracking Sensors Setup ---
# For dual-axis, you ideally want 2 or 4 tracking points to compare light.
# Let's assume you have an East UV sensor and a West UV sensor for tracking.
# uv_left = ADC(Pin(34))         # Safe ADC1 pin

# --- Cloudy Day Tracking Recovery State Variables ---
# cloudy_timer_start = None
# is_cloudy_standby = False
# CLOUD_THRESHOLD = 400       # Adjust based on real UV readings in shadows/clouds
# CLOUD_TIMEOUT = 900         # 15 minutes = 900 seconds
# RESUME_THRESHOLD = 600      # UV level required to declare clear skies again

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
    
#     # Background DNS Server (Port 53) to force mobile phones to auto-pop the portal page
#     dns_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     dns_sock.bind(('0.0.0.0', 53))
#     dns_sock.setblocking(False)

#     # Portal Web Server (Port 80)
#     web_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     web_sock.bind(('0.0.0.0', 80))
#     web_sock.listen(5)
#     web_sock.setblocking(False)
    
#     while True:
#         # 1. Handle DNS Interception
#         try:
#             data, addr = dns_sock.recvfrom(1024)
#             packet = data[:2] + b'\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00' + data[12:]
#             packet += b'\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04\xc0\xa8\x04\x01'
#             dns_sock.sendto(packet, addr)
#         except OSError:
#             pass

#         # 2. Handle HTTP Routing
#         try:
#             conn, addr = web_sock.accept()
#             request = conn.recv(1024).decode('utf-8')
            
#             # Form actions update to GET implicitly for lightweight parsing
#             if "GET /save" in request:
#                 try:
#                     # Isolate query string params
#                     url_path = request.split(' ')[1]
#                     query_string = url_path.split('?')[1]
#                     pairs = query_string.split('&')
                    
#                     params = {}
#                     for pair in pairs:
#                         if '=' in pair:
#                             key, val = pair.split('=')
#                             val = val.replace('+', ' ')
#                             # Basic URL Decoding for special symbols/spaces
#                             if '%' in val:
#                                 chunks = val.split('%')
#                                 clean_val = chunks[0]
#                                 for chunk in chunks[1:]:
#                                     if len(chunk) >= 2:
#                                         clean_val += chr(int(chunk[:2], 16)) + chunk[2:]
#                                     else:
#                                         clean_val += chunk
#                                 val = clean_val
#                             params[key] = val
                    
#                     ssid = params.get('ssid', '')
#                     password = params.get('password', '')

#                     # Output parsed inputs directly to your json configuration schema
#                     config_data = {"ssid": ssid, "password": password}
#                     with open("wifi_config.json", "w") as f:
#                         f.write(json.dumps(config_data))
                    
#                     print(f"[PORTAL]: Saved network '{ssid}' to wifi_config.json")
                    
#                     # Return success message to user mobile client browser
#                     conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
#                     conn.send('<html><body style="font-family:Arial;text-align:center;padding-top:50px;">')
#                     conn.send('<h2>Credentials Saved!</h2><p>Solar Tracker is now connecting...</p></body></html>')
#                     conn.close()
                    
#                     time.sleep(2)
#                     machine.reset() # Reboot cleanly to break loop execution
                    
#                 except Exception as parse_err:
#                     print("[PORTAL ERROR]: Form parsing error:", parse_err)
#                     conn.send('HTTP/1.1 400 Bad Request\r\n\r\n')
#                     conn.close()
            
#             # Default fallthrough behavior: Stream your beautiful external file
#             else:
#                 conn.send('HTTP/1.1 200 OK\r\n')
#                 conn.send('Content-Type: text/html\r\n')
#                 conn.send('Connection: close\r\n\r\n')
                
#                 try:
#                     with open('portal.html', 'r') as f:
#                         while True:
#                             chunk = f.read(512)
#                             if not chunk:
#                                 break
#                             conn.send(chunk)
#                 except OSError:
#                     conn.send('<html><body><h3>Error: portal.html file not found.</h3></body></html>')
                
#                 conn.close()
#         except OSError:
#             pass
            
#         time.sleep(0.05)
   
#     while True:
#         try:
#             conn, addr = portal_socket.accept()
#             req = conn.recv(1024).decode('utf-8')
            
#             if "POST /save" in req:
#                 # Extract payload data from form inputs manually
#                 body = req.split("\r\n\r\n")[-1]
#                 params = {}
#                 for item in body.split("&"):
#                     k, v = item.split("=")
#                     params[k] = v.replace("%20", " ") # Basic space character decoding
                
#                 # Save data to your internal storage system flash partition
#                 with open("wifi_config.json", "w") as f:
#                     f.write(json.dumps(params))
                
#                 success_response = "HTTP/1.1 200 OK\r\n\r\n<h3>Credentials Saved! Rebooting system...</h3>"
#                 conn.send(success_response.encode('utf-8'))
#                 conn.close()
#                 time.sleep(2)
                
#                 portal_socket.close()
#                 machine.reset() # Perform clean reset to connect to the new network
                
#             else:
#                 conn.send(portal_html.encode('utf-8'))
#                 conn.close()
#         except Exception as err:
#             print("[PORTAL ERROR]:", err)

#  WARNING! The ESP32 Wi-Fi Conflict Rule: The ESP32 has two Analog-to-Digital Converters:
#  ADC1 and ADC2. ADC2 completely shuts down whenever Wi-Fi is actively running. 
#  Since your code uses a Wi-Fi server, you MUST plug your analog sensors into ADC1 pins,
#  or your code will crash or read zeros. Safe ADC1 Pins to use: GPIO 32, GPIO 33, GPIO 34, 
#  GPIO 35, GPIO 36, GPIO 39.

print("modules imported...")
# Initial security pin generation
verification_code = random.randint(111111, 999999)
print(f"verification code created: {verification_code}")

s1 = None
s2 = None
sw1 = None
sw2 = None

#  def mov_servo(valx, valy):
#      if valx is not None and valy is not None:
#         duty_x = int(40 + (int(valx) / 180) * 75)
#         duty_y = int(40 + (int(valy) / 180) * 75)
#
#         servo_x.duty(duty_x)
#         servo_y.duty(duty_y)
#         pass

# --- Single Sensor Tracking State Variables ---
# last_uv_value = 0
# tracking_direction = 2 # Moves +2 degrees at a time. Changes to -2 if wrong way.

# --- Standby State Variables ---
# last_ping_time = time.time()
# TIMEOUT_SECONDS = 120         # 2 minutes
# server_active = True          # Tracks if the web server is running

# def process_automation():
    # """Handles rain safety, cloud survival standby, and active single-UV scanning."""
    # global s1, s2, sw1, sw2, last_uv_value, tracking_direction, cloudy_timer_start, is_cloudy_standby
    
    # # 1. READ ALL ACTUAL HARDWARE DATA
    # # rain_val = rain_sensor.read() 
    
    # # uv_val = uv_sensor.read()

    # # 2. SAFETY CHECK: Priority rain system overrides everything else
    # if rain_val < 2000: 
    #     print("[SAFETY ALERT]: Rain detected! Flattening solar panel!")
    #     sw1 = "Disabled" 
    #     s1, s2 = 90, 0           
    #     move_servos(s1, s2)
    #     return 

    # # 3. AUTOMATION STATE MANAGEMENT
    # if sw2 == "Auto":
    #     # Check if the sky is too dark/cloudy to hunt properly
    #     if uv_val < CLOUD_THRESHOLD:
    #         if not is_cloudy_standby:
    #             if cloudy_timer_start is None:
    #                 cloudy_timer_start = time.time()
    #                 print("[AUTOMATION]: UV drops below clear sky threshold. Monitoring clouds...")
    #             elif time.time() - cloudy_timer_start > CLOUD_TIMEOUT:
    #                 # Cloud timer expired! Activate safety standby mode
    #                 is_cloudy_standby = True
    #                 print("[POWER SAVER]: Overcast skies detected for 15 mins. Parking tracker in Eco-Standby.")
    #                 s1 = 90 # Center horizontal alignment safely
    #                 move_servos(s1, s2)
    #         return # Skip scanning adjustments while sky is completely dark
            
    #     # Recover from cloud tracking hold if the sun shines brightly again
    #     if is_cloudy_standby and uv_val >= RESUME_THRESHOLD:
    #         print("[AUTOMATION]: Clear skies detected! Resuming active UV scanning loops.")
    #         is_cloudy_standby = False
    #         cloudy_timer_start = None

    #     # Execute Active Scanning if sky status markers return to clear values
    #     if not is_cloudy_standby:
    #         cloudy_timer_start = None # Reset verification timers
    #         print(f"[AUTOMATION]: Scanning with Single UV Sensor. Strength: {uv_val}")
            
    #         if s1 is None: s1 = 90
    #         deadzone = 50 
            
    #         if abs(uv_val - last_uv_value) > deadzone:
    #             if uv_val < last_uv_value:
    #                 tracking_direction = -tracking_direction
    #                 print("[AUTOMATION]: Light dropping. Reversing tracking vector direction!")
                
    #             s1 = max(0, min(180, s1 + tracking_direction))
                
    #         last_uv_value = uv_val
    #         move_servos(s1, s2)
    # else:
    #     # Fall back completely to user mobile UI preferences if Manual control is active
    #     move_servos(s1, s2)

# class SPITerminal:
#     """Acts as a virtual serial port to automatically clone prints to the screen."""
#     def __init__(self, display_device):
#         self.display = display_device
#         self.lines = []
#         self.max_lines = 8

#     def write(self, b):
        # 1. Convert incoming raw serial bytes into a readable string
#         text = b.decode('utf-8')
        
        # Ignore empty newlines or carriage returns that mess up layouts
#         if text == '\n' or text == '\r\n' or not text.strip():
#             return len(b)
            
        # 2. Add the terminal text to our line tracker array
#         self.lines.append(text.strip())
        
        # 3. Scroll text if it hits the bottom of the screen
#         if len(self.lines) > self.max_lines:
#             self.lines.pop(0)
            
        # 4. Draw the live console lines onto the physical display screen
        # self.display.fill(0) # Clear Screen
#         for index, line in enumerate(self.lines):
            # self.display.text(line, 2, index * 12, 0xFFFF)
#             pass
            
#         return len(b) # Must return byte length to prevent serial lockup

def parse_http_request(client_socket):
    """Processes incoming data streams from your computer network."""
    global verification_code, s1, s2, sw1, sw2
#    global last_ping_time # uncomment this and add to the global ontop if using esp32
    try:
            # === DESKTOP PC SETTING ===
        # Read the whole request at once using recv()
        print("reading https request line...")
        raw_data = client_socket.recv(4096)
        if not raw_data:
            return
        request_line = raw_data.decode('utf-8')

        # Split headers from body
        parts = request_line.split("\r\n\r\n", 1)
        header_section = parts[0]
        body = parts[1] if len(parts) > 1 else ""

        # Get method
        lines = header_section.split("\r\n")
        if not lines or len(lines[0].split()) < 2:
            return
        method = lines[0].split()[0]

        # === ESP32 SETTING (Comment out everything below for PC) ===
        # print("reading https request line...")
        # request_line_bytes = client_socket.readline()
        # 1. Read the HTTP request line (e.g., "GET / HTTP/1.1")
        # print("reading https request line...")
        # request_line_bytes = client_socket.readline()
        # if not request_line_bytes:
        #    return
        # request_line = request_line_bytes.decode('utf-8').strip()
        
        # parts = request_line.split()
        # if len(parts) < 2:
        #    return
            
        # method = parts[0]  # Extracts exactly "GET" or "POST"

        # 3. Handle incoming POST data requests
        content_length = len(body) if body else 0
        print("handling incoming POST/GET data requests....")
        if method == 'POST':
            if content_length > 0:
                try:
                    app_data = json.loads(body)
                    
                    print(f"--> RAW STRING COMING FROM MIT APP INVENTOR: {body}") # Add this!

                    incoming_s1 = app_data.get("pos_servo_x")
                    incoming_s2 = app_data.get("pos_servo_y")
                    incoming_sw1 = app_data.get("flatPanelEnabled")
                    incoming_sw2 = app_data.get("manualOrAutoControl")
                    verification = app_data.get("verificationInput")
                    endConnection = app_data.get("endConnection")

                    if incoming_s1 is not None: s1 = incoming_s1
                    if incoming_s2 is not None: s2 = incoming_s2
                    if incoming_sw1 is not None: sw1 = incoming_sw1
                    if incoming_sw2 is not None: sw2 = incoming_sw2
                    
                    print(f"Data received successfully! Saved s1 as: {s1}, s2 as: {s2}, sw1 as: {sw1}, sw2 as: {sw2}.")

                    if verification and str(verification) == str(verification_code):
                        verification_code = "verified!"
                        
                except Exception as json_error:
                    print(f"[JSON ERROR]: Failed to parse payload. Reason: {json_error}")
            
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection: close\r\n\r\nData processed successfully!"
            client_socket.sendall(response.encode('utf-8')) # Use this for PC
            # client_socket.write(response.encode('utf-8')) # Use this for ESP32

        # 4. Handle incoming GET requests
        elif method == 'GET':
            if verification_code == "verified!":
                if 's1' not in globals() or s1 is None:
                    data_to_send = {"servo_x": "null","servo_y": "null","flatPanelEnabled": "null","manualOrAutoControl": "null"}
                else:
                    data_to_send = {"servo_x": f"{s1}","servo_y": f"{s2}","flatPanelEnabled": f"{sw1}","manualOrAutoControl": f"{sw2}"}
            else:
                data_to_send = {
                    "status": "success", 
                    "message": "Connection to server backend successful.", 
                    "verification_code": str(verification_code)
                }
                
            response_body = json.dumps(data_to_send)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n{response_body}"
            client_socket.sendall(response.encode('utf-8')) # Use this for PC
            # client_socket.write(response.encode('utf-8')) # Use this for ESP32
            
    except Exception as general_err:
        print(f"[STREAM ERROR]: Connection closed unexpectedly. Reason: {general_err}")

# def check_power_saving_mode(server_socket):
#     """Closes network hardware if phone is missing, but keeps loop alive."""
#     global last_ping_time, server_active, wlan
    
#     current_time = time.time()
    
    # If the phone is gone for 2 minutes and the server is still running
#     if server_active and (current_time - last_ping_time > TIMEOUT_SECONDS):
#         print("[ENERGY SAVER]: Phone disconnected for 2 minutes.")
#         print("Shutting down Web Server and Wi-Fi to save battery...")
        
#         try:
#             server_socket.close() # Shut down port 8000 safely
#         except:
#             pass
            
        # wlan.active(False)    # Turn off the ESP32 Wi-Fi antenna hardware
        server_active = False   # Mark server as offline
        print("[ENERGY SAVER]: Standing by. Sensor tracking is still active!")

def run():
    # global server_active ESP32 only 

    # 1. Initialize network manager first
    # If it fails, script halts here while broadcasting setup portal webpage
    # if not connect_wifi():
    #     return     

    print("init server_esp32.py locally...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("PASS!")
    
    # CHANGED: 0.0.0.0 opens the server up to your entire home network
    print("init httpd on port 8000...")
    s.bind(('0.0.0.0', 8000)) 
    s.listen(5)

    # === SETBLOCKING MODE ===
    # For Desktop PC: Comment out the line below (Leave it blocking)
    # For ESP32 Hardware: Uncomment the line below (Must be non-blocking)
    # s.setblocking(False) 

    # Activate the mirror hook
    # virtual_terminal = SPITerminal(display)
    # os.dupterm(virtual_terminal) # <--- THIS IS THE MAGIC LINE!

    print("PASS!")

    print("Server is running and ready to receive app data...")
    print("""
             /$$$$$$$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$         /$$$$$$                                                          /$$    /$$   /$$  
            | $$_____/ /$$__  $$| $$__  $$ /$$__  $$ /$$__  $$       /$$__  $$                                                        | $$   | $$ /$$$$  
            | $$      | $$  \__/| $$  \ $$|__/  \ $$|__/  \ $$      | $$  \__/  /$$$$$$   /$$$$$$  /$$    /$$ /$$$$$$   /$$$$$$       | $$   | $$|_  $$  
            | $$$$$   |  $$$$$$ | $$$$$$$/   /$$$$$/  /$$$$$$/      |  $$$$$$  /$$__  $$ /$$__  $$|  $$  /$$//$$__  $$ /$$__  $$      |  $$ / $$/  | $$  
            | $$__/    \____  $$| $$____/   |___  $$ /$$____/        \____  $$| $$$$$$$$| $$  \__/ \  $$/$$/| $$$$$$$$| $$  \__/       \  $$ $$/   | $$  
            | $$       /$$  \ $$| $$       /$$  \ $$| $$             /$$  \ $$| $$_____/| $$        \  $$$/ | $$_____/| $$              \  $$$/    | $$  
            | $$$$$$$$|  $$$$$$/| $$      |  $$$$$$/| $$$$$$$$      |  $$$$$$/|  $$$$$$$| $$         \  $/  |  $$$$$$$| $$               \  $/    /$$$$$$
            |________/ \______/ |__/       \______/ |________/       \______/  \_______/|__/          \_/    \_______/|__/                \_/    |______/  
                                                                                                                                             """)
    
    print("""
....................................................................................................
....................................................................:...............................
................+*..............+%:.......-%+--+#%#+:.............-%+..................+%...........
................%:...............:%+.......@.......:+%%-.........*#....................=%-..........
...............-@..................*%:.....#+..........=%*......+%.....................:@...........
...............#+...................-%+....:@............:##-..=%.......................@...........
..............:%......................*%-...-@:.............*%=%:.......................@...........
..............:%.......................:@+-*@%@%.............:%%........................@...........
..............:%........................+#-.............................................@...........
..............:%.....................+%#=....:::::......................................@...........
..............:%.....................:::=====-::::......................................@...........
..............:%.......................................................................-#...........
..............:%.......................................................................=*...........
...............%.......................................................................**...........
...............#-.....................................................................-@:...........
...............-#.....................................................................#*............
...............:%:.........................................::::-=*###*#####:.........=%.............
................=#.......*######**#@%%%%%%#:..............%%%%%%##.....%-...........=%-.............
.................#*........=%:....:@%%%%%%%=.............-@%%%%%%@:....:@:........-%#...............
..................#+.......%=.....=%%%%%%%@=.............-@%%%%%%@:.....*%......+@=.................
...........:::.....+%=....-#......=%%%%%%%%=.............-%%%%%%%@:.....:%:...#%##::=++*@...........
...........:@+*###*%%%+...**......=%%%%%%%@=.............-@%%%%%%%.......@:...........-%=...........
............-%:...........#-......:@%%%%%%#...............%%%%%%@=.......@:..........#*.............
.............:%*..........#*.......+@%%%%%:................%%%%%:.......:@:........#%:..............
...............-%*:.......:%-.......:+##=....:=+++.......................:.......+%-................
.................:*%....:-:...................::::...................-+:.:=.....-#:.................
..................%...++:-+.-**....................................:*+*-*+........%+................
.................%+......**+-............................:#...........=+:..........##...............
................#*........................-...:#%=*#%#+*%%-.........................+%-.............
...............:@.........................-#@#+.....................................:**.............
................@#====#%%@+............................................-%%-+%%%%%%**:...............
..........................:+%#=:..................................:+%%#=............................
..............................:-%@@%%-........................-%#=-.................................
...............................:@=..+#@@@@%=.....................#-.................................
................................:%*..............................:#*................................
..................................+@-..............................*#...............................
....................................-%%.............................#*..............................
....................................*%=..............................%-.............................
..................................-%-................................-@:............................
.................................:@=-+++..............................=%............................
......................................-%...............................*#...........................
......................................#:...............................-%...........................
.....................................#*.................................%-..........................
.....................................%:.................................#=..........................
....................................*#..................................-@..........................
                                                                """)
    
    print("In the case of an unfortunate disconnection, reconnect to port 8000.")
    print("Welcome to the ESP32 Python Server! It's lonely here....")

    while True:
        # process_automation() Run auto. and sensors...
        # check_power_saving_mode(s) check timer status..
        # if server_active:
            try:
                client_socket, addr = s.accept()

                #Desktop code...
                parse_http_request(client_socket)
                client_socket.close()

                # If we get here, a real connection came in from your app
                # ESP32 code.. uncomment when using
                #client_file = client_socket.makefile('rwb', buffering=0)
                #parse_http_request(client_file)
                #client_file.close()
                #client_socket.close()

                #process_automation()
            
            except KeyboardInterrupt:
                # This will now capture instantly without needing your app to ping it!
                print("\n[SHUTDOWN]: Keyboard interrupt detected (Ctrl+C).")
                print("Closing server sockets and exiting process... Goodbye!")
                s.close()
                sys.exit(0)

            except OSError:
                # ON ESP32: This triggers instantly when no one is connecting,
                # allowing your real-time sensor tasks below to run.
                # ON PC: This block is ignored because the server sleeps at s.accept().
                # === SENSOR AUTOMATION ===
                # process_automation()
                pass
        # else:
        #     process_automation()
        #     time.sleep(0.05)

        # tiny delay to keep exec. loops clean
        # time.sleep(0.02)

if __name__ == '__main__':
    run()

