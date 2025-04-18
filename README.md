# Auto-Lock-Using-Bluetooth-Proximity

This Python project automatically locks your Windows PC when a specific Bluetooth device (like your smartwatch or fitness band) goes out of range. It's your digital watchdog—if you're not nearby, your PC locks itself for security. 🕵️‍♂️💻

🚀 Features

- 🔍 **Scans Bluetooth devices** in real-time using `bleak`
- 🎯 Locks only when your **target device** is out of range
- 🕒 Includes a **grace period** before locking (configurable)
- 📶 Warns when the Bluetooth signal is weak
- 🔔 **Windows toast notifications** to keep you informed
- 🧠 Smart enough to avoid false positives

 
🛠️ Requirements

- Python 3.8+
- Windows 10 or higher
- A Bluetooth adapter on your PC
- Target BLE device (smartwatch, fitness band, etc.)
- Install dependencies:
   pip install bleak win10toast


📦 Installation

1. Clone this repo:
https://github.com/NageshMange/Auto-Lock-Using-Bluetooth-Proximity.git

⚙️ Configuration

Update the following values in `main.py`:

- `TARGET_DEVICE_NAME = "ColorFit Cadet"`  
  Name of your Bluetooth device (used for logging).

- `TARGET_DEVICE_ADDRESS = "F7:F6:DB:64:91:E8"`  
  The MAC address of your device (used for identification).

- `SCAN_INTERVAL = 5`  
  Time (in seconds) between each Bluetooth scan.

- `GRACE_PERIOD = 15`  
  Time (in seconds) to wait before locking the screen after the device is lost.

- `MIN_RSSI = -70`  
  Minimum acceptable signal strength (RSSI); lower means weaker signal.
             

▶️ Running the Script

  Simply run:-
- python main.py


🧪 Tested On

- Windows 11 
- ColorFit Cadet smartwatch
- Python 3.11


🧠 Use Case

Ideal for:-
- Preventing unauthorized access when you step away from your computer.
  Automatically locking your PC without relying on idle timers.


📝 macOS/Linux support not included due to use of Windows-specific lock API (rundll32.exe).
